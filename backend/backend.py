#!/usr/bin/env python
import pprint  # For printing JSON

import requests  # For getting weather from wttr.in
import json  # For parsing wttr.in response
import datetime  # For getting current time
import threading  # For threading
from pymongo.errors import ServerSelectionTimeoutError  # For checking if MongoDB is running
import configparser  # For reading config file
import database  # For database operations
import fcntl  # For locking file (Read/Write)

# Server Config
config = configparser.ConfigParser()
config.read('../Config/config.ini')
FILE_DB = config.get('FILE_DB', 'FILE_PATH')


# Parse wttr.in response and return a dictionary
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
    key = (json_object["nearest_area"][0]["country"][0]["value"] + ", " + str(region) + ", " +
           json_object["weather"][0]["date"])

    payload[key] = {"current_condition": current_condition, "hourly": payload_hourly_list, "weather": weather}

    return payload


# Get weather from wttr.in and save to database
def get_weather_from_WTTRIN(Country):
    # Change all spaces to + and capitalize all first letters
    country = Country.replace(" ", "+").title()
    # Get weather from wttr.in
    site = "https://wttr.in/" + country + "?format=j1"
    try:
        # Get weather from wttr.in with timeout of 5 secs
        weather_req = requests.get(site, timeout=5)
    # Catch exceptions
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to wttr.in")
        return None
    except requests.exceptions.ReadTimeout:
        print("Error: Read timeout")
        return None

    # If location is not found, return None
    if b'Unknown location;' in weather_req.content:
        return None

    # JSON object of weather
    weather_json = weather_req.json()

    # Generate payload
    payload = wttr_in_payload_generation(weather_json)  # This payload will be saved to database

    # save payload to file (This is the payload that will be sent to the frontend)
    save_payload_to_file(payload)

    # Save payload to database
    # Only payload will be saved to database
    # run function with timeout of 15 secs
    try:
        t = threading.Timer(15.0, save_weather_to_database, [payload])
        t.start()
    except:
        print("Error: Could not save to database")
    return payload


# Save weather to file Database (Payload)
def save_payload_to_file(json_object):
    payload = {}

    # Create file if it does not exist
    with open(FILE_DB, "a") as outfile:
        outfile.close()

    # Acquire file lock
    with open(FILE_DB, "r") as f:
        fcntl.flock(f, fcntl.LOCK_EX)

        # Check if file is empty
        if (open(FILE_DB, "r").read() == ""):
            with open(FILE_DB, "w") as outfile:
                # Key for each entry in the payload is the key in json_object
                key = list(json_object.keys())[0]
                payload[key] = json_object[key]
                json.dump(payload, outfile, indent=4)
                outfile.close()
                fcntl.flock(f, fcntl.LOCK_UN)
                return

        # read in a list of dictionaries
        with open(FILE_DB, "r") as outfile:
            try:
                payload = json.load(outfile)
            except json.decoder.JSONDecodeError:
                print("Error: Could not decode JSON")
                fcntl.flock(f, fcntl.LOCK_UN)
                return

        # Key for each entry in the payload is the key in json_object
        key = list(json_object.keys())[0]
        payload[key] = json_object[key]

        with open(FILE_DB, "w") as outfile:
            json.dump(payload, outfile, indent=4)
            outfile.close()

        # Release file lock
        fcntl.flock(f, fcntl.LOCK_UN)


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
    else:
        exist = get_weather_from_database(country, areaName, date)
        if exist is None:
            d.insert_one(payload)
            print("Weather forecast for country does not exist, inserting payload now")
        else:
            print("Weather forecast for country already exists, here it is")


def get_weather_from_database(country, areaName, date):
    # Return payload if found in database
    key = country + ", " + areaName + ", " + date
    # return None instead
    d = database.Database()
    if d.get_weather_from_database(key) is not None:
        return d.get_weather_from_database(key)
    else:
        return None


def frontend_get_weather(country, areaName):  # This function will be called by frontend
    # Make sure country and areaName are in title case
    country = country.title()
    # Get current date
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    date = "2023-03-24"
    # If areaName is empty, set it to country
    if areaName == "":
        areaName = country.title()
    # Get weather from database
    try:
        weather_payload = get_weather_from_database(country, areaName, date)
    except ServerSelectionTimeoutError:
        print("Database connection failed")
        weather_payload = None

    if weather_payload:
        return weather_payload
    else:
        # If not found, get weather from WTTRIN
        weather_payload = get_weather_from_WTTRIN(country)
        print("Sent Weather from WTTRIN")
        if weather_payload is None:
            # This is just a backup in case the database is empty
            weather_payload = get_weather_from_file(country, areaName, date)
            print("Sent Weather from file")
            return weather_payload
    return weather_payload


def get_weather_from_file(country, areaName, date):
    ret_payload = {}
    # Get weather from database
    key = country + ", " + areaName + ", " + date
    with open(FILE_DB, "r") as outfile:
        payload_dict = json.load(outfile)
        outfile.close()
    try:
        ret_payload[key] = payload_dict[key]
    except KeyError:
        ret_payload = None

    return ret_payload


def main():
    pass


if __name__ == '__main__':
    main()
