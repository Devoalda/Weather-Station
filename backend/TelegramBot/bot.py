# pip install pyTelegramBotAPI
import telebot
import json
from socket import *
import ssl
import time
import sys
import threading
import configparser

# Server Config
config = configparser.ConfigParser()
config.read('../../Config/config.ini')
SERVER_PORT = int(config.get('backendServer', 'Port'))
SERVER_IP = config.get('backendServer', 'IP')
CERT = config.get('SSL', 'Cert')
TOKEN = config.get('TELEGRAM_BOT', 'Token')
CHANNEL_ID = config.get('TELEGRAM_BOT', 'CHANNEL_ID')

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("Received: " + message.text + " from " + str(message.chat.id))
    bot.send_message(message.chat.id, "Welcome to WeatherBot! Type /help to see available commands.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    # Display help message
    print("Received: " + message.text + " from " + str(message.chat.id))
    bot.reply_to(message, """Available commands:
    /start - Start the bot
    /help - Display this message
    /weather <Country> - Get the weather for a location
    """)


@bot.message_handler(commands=['weather'])
def handle_help(message):
    # Display help message
    print("Received: " + message.text + " from " + str(message.chat.id))
    try:
        country = message.text.split(" ")[1]
    except IndexError:
        bot.reply_to(message, "Please enter a country!")
        return
    weather_string = get_weather(country)
    bot.reply_to(message, weather_string)


def get_weather_from_Server(country):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('../SSL/certificate.pem')
    context.check_hostname = False

    clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=SERVER_IP)
    try:
        clientSocket.connect((SERVER_IP, SERVER_PORT))
    except ConnectionRefusedError:
        print("Connection refused!")
        return None

    clientSocket.send(country.encode())
    buffer = 10240
    data = clientSocket.recv(buffer).decode()
    if data == "Error":
        payload = None
    else:
        payload = json.JSONDecoder().decode(data)
    clientSocket.close()
    return payload


def get_weather(country):
    payload = get_weather_from_Server(country)
    if payload is None:
        return "Error! Country not found!"
    else:
        key = list(payload.keys())[0]
        weather_desc = payload.get(key).get("current_condition").get("weatherDesc")
        weather_temp = payload.get(key).get("current_condition").get("temp_C")
        country = payload.get(key).get("current_condition").get("country")
        return "[WEATHER UPDATE]\nThe weather in " + country + " is " + weather_desc + " at " + weather_temp + " degrees Celsius."


def SG_channel_Update(payload):
    if payload is None:
        return None
    else:
        key = list(payload.keys())[0]
        weather_desc = payload.get(key).get("current_condition").get("weatherDesc")
        weather_temp = payload.get(key).get("current_condition").get("temp_C")
        country = payload.get(key).get("current_condition").get("country")
        return "☁️[WEATHER UPDATE]☁️\nThe weather in " + country + " is " + weather_desc + " at " + weather_temp + " degrees Celsius."


def sgCheckRainy(payload):
    if payload is None:
        return None
    else:
        # 24 Hour time in 4 digits
        current_time_24hr = time.strftime("%H%M")
        print("Current time: " + current_time_24hr)
        key = list(payload.keys())[0]
        hourly_list = payload.get(key).get("hourly")
        closest_time = 2400

        # Find the closest time to the current time
        for item in hourly_list:
            if int(current_time_24hr) < int(item.get("time")) < closest_time:
                closest_time = int(item.get("time"))

        if closest_time == 2400:
            closest_time = 0

        print("Closest time: " + str(closest_time))
        for item in hourly_list:
            # Find the closest time with closest_time
            if int(item.get("time")) == int(closest_time):
                chance_rain = item.get("chancerain")
                print("Chance of rain: " + str(chance_rain))
                if int(chance_rain) >= 50:
                    return "⛈️[RAIN ALERT]⛈️\nIt may rain soon!\nLocation: " + payload.get(key).get(
                        "current_condition").get("country") + "\nTime Now: " + str(
                        current_time_24hr) + "\nTime: " + str(closest_time) + "\nChance of rain: " + str(
                        chance_rain) + "%"

        return None


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "I don't understand what you mean. Type /help to see available commands.")


# Periodically send weather updates
def send_weather_updates():
    # Fix the logic of this
    while True:
        payload = get_weather_from_Server("Singapore")
        update = SG_channel_Update(payload)
        if update is None:
            print("Error! Weather update failed!")
            bot.send_message(CHANNEL_ID, "Error! Weather update failed!")
        else:
            print("Weather update sent!")
            bot.send_message(CHANNEL_ID, SG_channel_Update(payload))

        time.sleep(60)  # Should be every hour/day but for Demo purposes, every minute


def send_rain_update():
    while True:
        payload = get_weather_from_Server("Singapore")
        rain = sgCheckRainy(payload)
        if rain is not None:
            print("Rain alert sent!")
            bot.send_message(CHANNEL_ID, rain)

        time.sleep(30)  # This can be every 1 hour but for Demo purposes, every 30 seconds


# send_rain_update()
# Multiple threads
def start_bot():
    try:
        bot.send_message(CHANNEL_ID, "The Weather Station bot is now online!")
        t = threading.Thread(target=send_weather_updates).start()
        s = threading.Thread(target=send_rain_update).start()
        bot.polling()
        # Catch SIGKILL
    except KeyboardInterrupt or SystemExit:
        bot.send_message(CHANNEL_ID, "The Weather Station bot is now offline!")
        print("Bot stopped.")
        sys.exit()


if __name__ == '__main__':
    start_bot()
