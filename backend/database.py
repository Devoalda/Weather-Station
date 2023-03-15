import pymongo
from datetime import date
import json
import datetime

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

    def delete_many(self):
        # Delete all data in database
        x = self.mycol.delete_many({})

    def print_all_data(self):
        # Print all data in database
        for y in self.mycol.find():
            return y
            #print(y)

    def get_weather_from_database(self, key):
        # Get weather from database
        return_dict = {}
        for i in self.mycol.find():
            res = list(i.keys())[1]
            if key == res:
                return_dict[key] = i[key]
                return return_dict
            else:
                return None
            
    def update(self, payload):
        for i in self.mycol.find():
            res = list(i.keys())[1]
            check = list(payload.keys())[0]
            if check == res:
                print(payload)

    #def update_country(self, key):
    #    x = self.mycol.update_one({key()}, {"$set": new_val})

#today = date.today()
#country = "Singapore, "
#city = "Singapore, "
#date = "2023-03-07"
#key = country + city + date
#get_weather_from_database(key)