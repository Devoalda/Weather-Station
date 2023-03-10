#!/usr/bin/env python
import ssl

import requests
import json
import datetime
import time, threading
from socket import *
from threading import Thread
from pprint import pprint
from datetime import date
import pymongo

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
    weather_json = requests.get(site).json()
    payload = wttr_in_payload_generation(weather_json)  # This payload will be saved to database
    #pprint(payload)

    # Save to file
    # All weather data will be saved to a file
    save_weather_to_file(weather_json)

    # save payload to file
    save_payload_to_file(payload)

    # Save payload to database
    # Only payload will be saved to database

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

def save_weather_to_file(json_object):
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
    with open(payload) as f:
        # for each dictionary in the list, load it into json and call it data
        data = json.load(f)

    Database.insert_many(data)

class Database():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.client["WeatherDatabase"]
        self.mycol = self.mydb["WeatherCollection"]  

    def insert_one(self, data):
        # Insert data into database
        x = self.mycol.insert_one(data)

    def insert_many(self, data):
        # insert many into database
        x = self.mycol.insert_many(data)

    def delete_many(self, data):
        # Delete all data in database
        x = self.mycol.delete_many({})

    def print_all_data(self):
        # Print all data in database
        for y in self.mycol.find():
            print(y)

    def get_weather_from_database(self, key):
        for i in self.mycol.find():
            res = list(i.keys())[1]
            if res == key:
                print(i)

#today = date.today()
#country = "Singapore, "
#city = "Singapore, "
#date = "2023-03-07"
#key = country + city + date
#get_weather_from_database(key)


def frontend_get_weather(country, areaName):  # This function will be called by frontend

    country = country.title()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(date)
    if areaName == "":
        areaName = country.title()
    # Get weather from database
    # If not found, get weather from WTTRIN
    weather_payload = get_weather_from_file(country, areaName, date)
    if weather_payload is None:
        print("here")
        weather_payload = get_weather_from_WTTRIN(country)
    # Save to database

    return weather_payload

def get_weather_from_file(country, areaName, date):
    return_payload = {}

    # Get weather from database
    key = country + ", " + areaName + ", " + date
    with open("payload_DB.json", "r") as outfile:
        payload_dict = json.load(outfile)
        outfile.close()

    try:
        return_payload = payload_dict[key]
    except KeyError:
        return_payload = None

    return return_payload

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


def main():
    #print(frontend_get_weather("Singapore",""))
    pass
    #cache_Singapore()
    #get_weather_from_WTTRIN("Singapore")
    #get_weather_from_WTTRIN("Vietnam")
    #get_weather_from_WTTRIN("Malaysia")
    #pprint(get_weather_from_WTTRIN("Thailand"))
    #get_weather_from_WTTRIN("Indonesia")
    #get_weather_from_WTTRIN("India")
    #get_weather_from_WTTRIN("China")
    #get_weather_from_WTTRIN("Japan")
    #get_weather_from_WTTRIN("South Korea")
    #get_weather_from_WTTRIN("Taiwan")

    #old_data_rubbish_collection()

    # pprint(frontend_get_weather("Singapore", "Singapore", "2020-05-10"))
    #tcpServer()



if __name__ == '__main__':
    main()
