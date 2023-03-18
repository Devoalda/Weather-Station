#!/usr/bin/env python
import ssl

import requests
import json
import datetime
import time, threading
from socket import *
from threading import Thread, Timer
from pprint import pprint
from datetime import date
import pymongo
from pymongo.errors import ServerSelectionTimeoutError

import database
from time import sleep


def wttr_in_payload_generation(json_object):
    payload = {}
    current_condition = {}
    payload_hourly_list = []

    weather = {}

    # Current Condition Dictionary
    current_condition["temp_C"] = json_object["current_condition"][0]["temp_C"]
    current_condition["humidity"] = json_object["current_condition"][0]["humidity"]
    current_condition["weatherDesc"] = json_object["current_condition"][0]["weatherDesc"][0]["value"]
    current_condition["windspeed"] = json_object["current_condition"][0]["windspeedKmph"]
    current_condition["winddir"] = json_object["current_condition"][0]["winddir16Point"]
    current_condition["country"] = json_object["nearest_area"][0]["country"][0]["value"]

    if json_object["nearest_area"][0]["region"][0]["value"] == "":
        current_condition["region"] = json_object["nearest_area"][0]["country"][0]["value"]
        region = json_object["nearest_area"][0]["country"][0]["value"]
    else:
        current_condition["region"] = json_object["nearest_area"][0]["region"][0]["value"]
        region = json_object["nearest_area"][0]["region"][0]["value"]

    # Hourly Dictionary
    hourly_list = json_object["weather"][0]["hourly"]
    for item in hourly_list:
        hourly = {}
        hourly["tempC"] = item["tempC"]
        hourly["time"] = item["time"]
        hourly["chancerain"] = item["chanceofrain"]
        hourly["chancethunder"] = item["chanceofthunder"]
        hourly["chancewindy"] = item["chanceofwindy"]
        hourly["precipMM"] = item["precipMM"]
        hourly["humidity"] = item["humidity"]
        hourly['DewPointC'] = item['DewPointC']
        hourly['visibility'] = item['visibility']
        hourly['cloudcover'] = item['cloudcover']
        hourly["weatherDesc"] = item["weatherDesc"][0]["value"]
        hourly["winddir16Point"] = item["winddir16Point"]
        hourly["windspeedKmph"] = item["windspeedKmph"]
        payload_hourly_list.append(hourly)

    # Weather Dictionary
    weather["maxtemp"] = json_object["weather"][0]["maxtempC"]
    weather["mintemp"] = json_object["weather"][0]["mintempC"]

    # Payload Dictionary
    # Key will be Country, areaName, Date
    key = (json_object["nearest_area"][0]["country"][0]["value"] + ", " + str(region) + ", " + json_object["weather"][0]["date"])

    payload[key] = {"current_condition": current_condition, "hourly": payload_hourly_list, "weather": weather}

    return payload


def get_weather_from_WTTRIN(Country):
    # Change all spaces to + and capitalize all first letters
    country = Country.replace(" ", "+").title()

    site = "https://wttr.in/" + country + "?format=j1"
    try:
        weather_req = requests.get(site, timeout=5)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to wttr.in")
        return None

    if b'Unknown location;' in weather_req.content:
        return None
    weather_json = weather_req.json()
    payload = wttr_in_payload_generation(weather_json)  # This payload will be saved to database
    # pprint(payload)

    # Save to file
    # All weather data will be saved to a file
    # save_weather_to_file(weather_json)

    # save payload to file (This is the payload that will be sent to the frontend)
    save_payload_to_file(payload)

    # Save payload to database
    # Only payload will be saved to database

    # run function with timeout of 5 secs
    try:
        # create a thread timer object
        # save_weather_to_database(payload)
        t = threading.Timer(15.0, save_weather_to_database, [payload])
        t.start()
    except:
        print("Error: Could not save to database")

    return payload


def save_payload_to_file(json_object):
    payload = {}
    file = "payload_DB.json"

    # Create file if it does not exist
    with open(file, "a") as outfile:
        outfile.close()

    # Check if file is empty
    if (open(file, "r").read() == ""):
        with open(file, "w") as outfile:
            # Key for each entry in the payload is the key in json_object
            key = list(json_object.keys())[0]
            payload[key] = json_object[key]
            json.dump(payload, outfile, indent=4)
            outfile.close()
            return

    # read in a list of dictionaries
    with open(file, "r") as outfile:
        payload = json.load(outfile)
        outfile.close()

    # Key for each entry in the payload is the key in json_object
    key = list(json_object.keys())[0]
    payload[key] = json_object[key]

    with open(file, "w") as outfile:
        json.dump(payload, outfile, indent=4)
        outfile.close()


def save_weather_to_file(json_object):  # May not be required but just in case cuz there's duplicates
    weather_list = []
    file = "weather.json"

    # Create file if it does not exist
    with open(file, "a") as outfile:
        outfile.close()

    # Check if file is empty
    if (open(file, "r").read() == ""):
        with open(file, "w") as outfile:
            weather_list.append(json_object)
            json.dump(weather_list, outfile, indent=4)
            outfile.close()
            return

    # read in a list of dictionaries
    with open(file, "r") as outfile:
        weather_list = json.load(outfile)
        outfile.close()

    weather_list.append(json_object)

    with open("weather.json", "w") as outfile:
        json.dump(weather_list, outfile, indent=4)
        outfile.close()


def save_weather_to_database(payload):
    # open the json file that has been saved

    keys = list(payload.keys())[0].split(", ")
    country = keys[0]
    areaName = keys[1]
    date = keys[2]

    country_name_date = country + ", " + areaName + ", " + date

    try:
        d = database.Database()
    except:
        print("Database connection failed")
        return

    if d.print_all_data() is None:
        d.insert_one(payload)
        print("Payload inserted")
        #print(payload)
        #check = list(payload.keys())[1]
        #print(check)
    else:
        exist = get_weather_from_database(country, areaName, date)
        #print(exist)
        #check = list(payload.keys())[0]
        if exist is None:
            d.insert_one(payload)
            print("Weather forecast for country does not exist, inserting payload now")
            #print(payload)
        else:
            print("Weather forecast for country already exists, here it is")
            #print(payload)


def get_weather_from_database(country, areaName, date):
    # Return payload if found in database
    # return None instead
    # Return payload if found in database
    key = country + ", " + areaName + ", " + date
    # return None instead
    d = database.Database()
    #print(country)
    #print(areaName)
    #print(date)
    #print(key)
    #print(d.get_weather_from_database(key))
    #d.print_all_data()
    if d.get_weather_from_database(key) is not None:
        #print(key)
        return d.get_weather_from_database(key)
    else:
        return None


def frontend_get_weather(country, areaName):  # This function will be called by frontend

    country = country.title()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # print(date)
    if areaName == "":
        areaName = country.title()
    # Get weather from database
    #weather_payload = None
    try:
        weather_payload = get_weather_from_database(country, areaName, date)
    except ServerSelectionTimeoutError:
        print("Database connection failed")
        weather_payload = None

    if weather_payload:
        #print(weather_payload)
        #print("Weather from database")
        return weather_payload
    else:
        # If not found, get weather from WTTRIN
        # This is just a backup in case the database is empty
        weather_payload = get_weather_from_WTTRIN(country)
        print("Weather from WTTRIN")
        if weather_payload is None:
            weather_payload = get_weather_from_file(country, areaName, date)
            print("Weather from file")
            return weather_payload
    return weather_payload

def get_weather_from_file(country, areaName, date):
    ret_payload = {}
    # Get weather from database
    key = country + ", " + areaName + ", " + date
    with open("payload_DB.json", "r") as outfile:
        payload_dict = json.load(outfile)
        outfile.close()
    try:
        ret_payload[key] = payload_dict[key]
    except KeyError:
        ret_payload = None

    return ret_payload


def old_data_rubbish_collection():
    # Get date 7 days ago (Can be changed to later date)
    date_to_delete = datetime.datetime.now().date() - datetime.timedelta(days=7)

    with open("weather.json", "r") as outfile:
        weather_list = json.load(outfile)
        outfile.close()

    # Delete all data older than 1 week
    for item in weather_list:
        item_date = item["weather"][0]["date"]
        if datetime.datetime.strptime(item_date, '%Y-%m-%d').date() < date_to_delete:
            weather_list.remove(item)

    with open("weather.json", "w") as outfile:
        json.dump(weather_list, outfile)
        outfile.close()


def get_latest_weather_from_file():
    file = "weather.json"
    weather_list = []

    with open(file, "r") as outfile:
        weather_list = json.load(outfile)
        outfile.close()

    return weather_list[-1]


def printKeys(json_object):
    for key in json_object:
        print(key)


def getAllWeatherDescriptions():
    with open("payload_DB.json", "r") as outfile:
        weather_dict = json.load(outfile)
        outfile.close()

    weather_descriptions = []
    for key in weather_dict:
        for item in weather_dict[key]["hourly"]:
            if item["weatherDesc"] not in weather_descriptions:
                weather_descriptions.append(item["weatherDesc"])
    return weather_descriptions


def main():
    pass
    #d = database.Database()
    #print(d.print_all_data())
    # print(get_weather_from_database("Singapore", "Singapore", "2023-03-15"))
    # pprint(frontend_get_weather("singapore",""))
    # get_weather_from_WTTRIN("antartica")
    # cache_Singapore()
    # pprint(get_weather_from_WTTRIN("Singapore"))
    # get_weather_from_WTTRIN("amazon")
    #get_weather_from_WTTRIN("singapore")
    #pprint(frontend_get_weather("Singapore", ""))
    # get_weather_from_WTTRIN("africa")
    # get_weather_from_WTTRIN("australia")
    # get_weather_from_WTTRIN("brazil")
    # get_weather_from_WTTRIN("canada")
    # other countries with various weather conditions
    # get_weather_from_WTTRIN("france")
    # get_weather_from_WTTRIN("germany")
    # get_weather_from_WTTRIN("greece")
    # get_weather_from_WTTRIN("india")

    # get_weather_from_WTTRIN("Malaysia")
    # pprint(get_weather_from_WTTRIN("Thailand"))
    # get_weather_from_WTTRIN("Indonesia")
    # get_weather_from_WTTRIN("India")
    # get_weather_from_WTTRIN("China")
    # get_weather_from_WTTRIN("Japan")
    # get_weather_from_WTTRIN("South Korea")
    # get_weather_from_WTTRIN("Taiwan")
    # get_weather_from_WTTRIN("Thailand")
    # get_weather_from_WTTRIN("Philippines")

    # old_data_rubbish_collection()

    # pprint(frontend_get_weather("Singapore", "Singapore", "2020-05-10"))
    # tcpServer()

    # print(getAllWeatherDescriptions())


if __name__ == '__main__':
    main()
