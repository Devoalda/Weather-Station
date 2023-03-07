import json
import pymongo
from datetime import date

with open('weather.json') as f:
    data = json.load(f)

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["WeatherDatabase"]
mycol = mydb["WeatherCollection"]  

# Insert data into database
x = mycol.insert_one(data)

# insert many into database
x = mycol.insert_many(data)

# delete many from database
x = mycol.delete_many({})

# Print all data in database
for y in mycol.find():
    res = list(y.keys())[1]
    print(y) 

# print data based on query
def query(key):
    for i in mycol.find():
        res = list(i.keys())[1]
        if res == key:
            print(i)

today = date.today()
country = "Singapore, "
city = "Singapore, "
date = "2023-03-07"
key = country + city + date
query(key)