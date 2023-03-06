from flask import Flask, render_template

app = Flask(__name__)
data = {'Vietnam, , 2023-03-03': {
    'current_condition': {'temp_C': '25', 'humidity': '43', 'weatherDesc': 'Sunny', 'windspeed': '9', 'winddir': 'NE',
                          'country': 'Vietnam', 'region': 'Vietnam'}, 'hourly': [
        {'DewPointC': '11', 'DewPointF': '52', 'FeelsLikeC': '12', 'FeelsLikeF': '54', 'HeatIndexC': '13',
         'HeatIndexF': '55', 'WindChillC': '12', 'WindChillF': '54', 'WindGustKmph': '13', 'WindGustMiles': '8',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '91', 'chanceofsnow': '0', 'chanceofsunshine': '88',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '18', 'humidity': '89', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1021', 'pressureInches': '30', 'tempC': '13', 'tempF': '55', 'time': '0',
         'uvIndex': '1', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Clear'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '41', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '6', 'DewPointF': '43', 'FeelsLikeC': '7', 'FeelsLikeF': '45', 'HeatIndexC': '9',
         'HeatIndexF': '47', 'WindChillC': '7', 'WindChillF': '45', 'WindGustKmph': '17', 'WindGustMiles': '10',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '93', 'chanceofsnow': '0', 'chanceofsunshine': '94',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '5', 'humidity': '85', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1021', 'pressureInches': '30', 'tempC': '9', 'tempF': '47', 'time': '300',
         'uvIndex': '1', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Clear'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '41', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '8', 'DewPointF': '47', 'FeelsLikeC': '9', 'FeelsLikeF': '48', 'HeatIndexC': '10',
         'HeatIndexF': '50', 'WindChillC': '9', 'WindChillF': '48', 'WindGustKmph': '16', 'WindGustMiles': '10',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '43',
         'chanceofrain': '0', 'chanceofremdry': '87', 'chanceofsnow': '0', 'chanceofsunshine': '81',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '26', 'humidity': '91', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1022', 'pressureInches': '30', 'tempC': '10', 'tempF': '50', 'time': '600',
         'uvIndex': '1', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '116',
         'weatherDesc': [{'value': 'Partly cloudy'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '37', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '10', 'DewPointF': '51', 'FeelsLikeC': '20', 'FeelsLikeF': '67', 'HeatIndexC': '20',
         'HeatIndexF': '67', 'WindChillC': '20', 'WindChillF': '67', 'WindGustKmph': '9', 'WindGustMiles': '6',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '80', 'chanceofsnow': '0', 'chanceofsunshine': '94',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '0', 'humidity': '55', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1022', 'pressureInches': '30', 'tempC': '20', 'tempF': '67', 'time': '900',
         'uvIndex': '5', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '39', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '11', 'DewPointF': '52', 'FeelsLikeC': '27', 'FeelsLikeF': '81', 'HeatIndexC': '27',
         'HeatIndexF': '81', 'WindChillC': '28', 'WindChillF': '82', 'WindGustKmph': '8', 'WindGustMiles': '5',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '96', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '91', 'chanceofsnow': '0', 'chanceofsunshine': '85',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '6', 'humidity': '36', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1019', 'pressureInches': '30', 'tempC': '28', 'tempF': '82', 'time': '1200',
         'uvIndex': '7', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '42', 'windspeedKmph': '7', 'windspeedMiles': '4'},
        {'DewPointC': '11', 'DewPointF': '52', 'FeelsLikeC': '27', 'FeelsLikeF': '80', 'HeatIndexC': '27',
         'HeatIndexF': '80', 'WindChillC': '27', 'WindChillF': '81', 'WindGustKmph': '9', 'WindGustMiles': '6',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '95', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '86', 'chanceofsnow': '0', 'chanceofsunshine': '91',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '5', 'humidity': '37', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1016', 'pressureInches': '30', 'tempC': '27', 'tempF': '81', 'time': '1500',
         'uvIndex': '7', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Sunny'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '38', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '13', 'DewPointF': '56', 'FeelsLikeC': '19', 'FeelsLikeF': '66', 'HeatIndexC': '19',
         'HeatIndexF': '66', 'WindChillC': '19', 'WindChillF': '66', 'WindGustKmph': '9', 'WindGustMiles': '6',
         'chanceoffog': '0', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '0',
         'chanceofrain': '0', 'chanceofremdry': '80', 'chanceofsnow': '0', 'chanceofsunshine': '94',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '3', 'humidity': '71', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1019', 'pressureInches': '30', 'tempC': '19', 'tempF': '66', 'time': '1800',
         'uvIndex': '1', 'visibility': '10', 'visibilityMiles': '6', 'weatherCode': '113',
         'weatherDesc': [{'value': 'Clear'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '43', 'windspeedKmph': '8', 'windspeedMiles': '5'},
        {'DewPointC': '13', 'DewPointF': '56', 'FeelsLikeC': '14', 'FeelsLikeF': '56', 'HeatIndexC': '14',
         'HeatIndexF': '57', 'WindChillC': '14', 'WindChillF': '56', 'WindGustKmph': '13', 'WindGustMiles': '8',
         'chanceoffog': '13', 'chanceoffrost': '0', 'chanceofhightemp': '0', 'chanceofovercast': '88',
         'chanceofrain': '0', 'chanceofremdry': '85', 'chanceofsnow': '0', 'chanceofsunshine': '6',
         'chanceofthunder': '0', 'chanceofwindy': '0', 'cloudcover': '57', 'humidity': '96', 'precipInches': '0.0',
         'precipMM': '0.0', 'pressure': '1023', 'pressureInches': '30', 'tempC': '14', 'tempF': '57', 'time': '2100',
         'uvIndex': '1', 'visibility': '2', 'visibilityMiles': '1', 'weatherCode': '143',
         'weatherDesc': [{'value': 'Mist'}], 'weatherIconUrl': [{'value': ''}], 'winddir16Point': 'NE',
         'winddirDegree': '46', 'windspeedKmph': '8', 'windspeedMiles': '5'}],
    'weather': {'maxtemp': '28', 'mintemp': '8'}}}

@app.route('/')
def index():  # put application's code here
    def getHumidity():
        air = data.get('Vietnam, , 2023-03-03').get("current_condition").get("humidity")
        circleProgress = {
            "css": "c100 p" + str(air) + " small center",
            "val": air
        }
        return circleProgress
    def getHourData():
        hourlyData = data.get('Vietnam, , 2023-03-03').get("hourly")
        return hourlyData
    context = {
        "labels": ["red", "green", "blue"],
        "values": [100, 200, 300],
    }
    return render_template("index.html", title="New title", context=context, humidity=getHumidity(), hourlyData=getHourData())


if __name__ == '__main__':
    app.run()

# print(data.get('Vietnam, , 2023-03-03').get("hourly")[0].get("time"))