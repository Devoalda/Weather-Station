import datetime
from flask import Flask, render_template, request, url_for, flash, redirect
import json
import requests
from socket import *
from pprint import pprint
import ssl

# https://ipinfo.io/json
app = Flask(__name__)
app.config['SECRET_KEY'] = '***REMOVED***'

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form['location']
        if not location:
            flash('Please enter a valid location')
        if location:
            flash('This is the entered ' + location)
            return redirect('location/country=' + location)

    return render_template('search.html')


@app.route('/location/<country>', methods=['GET', 'POST'])
def index(country):  # put application's code here
    def get_weather_from_Server(country):
        # Server Config
        # Change IP to your server IP
        serverIP = "192.168.137.10"
        serverPort = 12000

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('../backend/SSL/certificate.pem')
        context.check_hostname = False

        clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=serverIP)
        clientSocket.connect((serverIP, serverPort))

        clientSocket.send(country.encode())
        buffer = 10240
        payload = json.JSONDecoder().decode(clientSocket.recv(buffer).decode())
        clientSocket.close()
        return payload

    apiData = get_weather_from_Server(country)

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

    def getHourData(apiData):
        res = list(apiData.keys())[0]
        hourlyData = apiData.get(res).get("hourly")
        print(hourlyData)
        return hourlyData

    def getDate():
        now = datetime.date.today()
        return now

    return render_template("index.html", date=getDate(), humidity=getHumidity(apiData),
                           hourlyData=getHourData(apiData), currentCondition=getCurrentCondition(apiData))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)