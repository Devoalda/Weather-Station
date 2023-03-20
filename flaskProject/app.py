import datetime
import pickle
from flask import Flask, render_template, request, url_for, redirect
import json
import requests
from socket import *
from pprint import pprint
import ssl
import re
import configparser
# https://ipinfo.io/json
app = Flask(__name__)
app.config['SECRET_KEY'] = '***REMOVED***'

# Configs
config = configparser.ConfigParser()
config.read('../Config/config.ini')
SERVER_PORT = int(config.get('backendServer', 'Port'))
SERVER_IP = config.get('backendServer', 'IP')
CERT = config.get('SSL', 'Cert')


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        resp = request.form['location']
        if resp is None:
            return redirect('404')
        if resp:
            return redirect('location/' + resp)
    return render_template('search.html')


@app.route('/location/<country>', methods=['GET', 'POST'])
def index(country):  # put application's code here
    def get_weather_from_Server(country):
        # Server Config
        # Change IP to your server IP
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(CERT)
            context.check_hostname = False

            clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=SERVER_IP)
            clientSocket.connect((SERVER_IP, SERVER_PORT))

            clientSocket.send(country.encode())
            buffer = 20480
            data = clientSocket.recv(buffer).decode()
            if data == "Error":
                payload = None
            else:
                payload = json.JSONDecoder().decode(data)
            clientSocket.close()
            print(payload)
            return payload
        except Exception as e:
            print("Error!!!")
            print(e)
            return None


    apiData = get_weather_from_Server(country)
    if apiData is None:
        return redirect(url_for('error404'))


    def countryRegionDetails(data):
        res = list(apiData.keys())[0].split(",")
        newList = [res[0].lstrip(), res[1].lstrip()]
        print("country:",newList[0])
        print("region:",newList[1])
        if newList[0] == newList[1]:
            print(True)
        return newList

    def getCurrentCondition(apiData):
        res = list(apiData.keys())[0]
        cd = apiData.get(res).get("current_condition")
        return cd

    def getHumidity(apiData):
        res = list(apiData.keys())[0]
        air = apiData.get(res).get("current_condition").get("humidity")
        circleProgress = {
            "css": "c100 p" + str(air) + " small center",
            "val": air
        }
        return circleProgress

    def getMinMaxWeather(apiData):
        res = list(apiData.keys())[0]
        minMaxTemp = apiData.get(res).get("weather")
        return minMaxTemp

    def getHourData(apiData):
        res = list(apiData.keys())[0]
        hourlyData = apiData.get(res).get("hourly")
        return hourlyData

    def getDate():
        now = datetime.date.today()
        return now

    location = country.capitalize()

    weatherType = {
        "Sunny": [""]
    }
    print(country)
    return render_template("index.html", date=getDate(), humidity=getHumidity(apiData),
                           countryRegion=countryRegionDetails(apiData),
                           hourlyData=getHourData(apiData), currentCondition=getCurrentCondition(apiData),
                           location=location, minMaxTemp=getMinMaxWeather(apiData))


@app.route('/404')
def error404():
    return render_template('404.html'), 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
