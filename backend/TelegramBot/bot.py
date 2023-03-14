# pip install pyTelegramBotAPI

import telebot
import json
from socket import *
import ssl
import time
import sys
import threading
#import backend as backend

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000

with open("secret.txt", "r") as f:
    TOKEN = f.readline()

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("Received: " + message.text + " from " + str(message.chat.id))
    bot.send_message(message.chat.id, "Welcome to WeatherBot! Type /help to see available commands.")


@bot.message_handler(commands=['help'])
def handle_help(message):
    # Display help message
    bot.reply_to(message, """Available commands:
    /start - Start the bot
    /help - Display this message
    /weather <Country> - Get the weather for a location
    """)


@bot.message_handler(commands=['weather'])
def handle_help(message):
    # Display help message
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


def SG_channel_Update():
    payload = get_weather_from_Server("Korea")
    if payload is None:
        return None
    else:
        key = list(payload.keys())[0]
        weather_desc = payload.get(key).get("current_condition").get("weatherDesc")
        weather_temp = payload.get(key).get("current_condition").get("temp_C")
        country = payload.get(key).get("current_condition").get("country")
        return "[WEATHER UPDATE]\nThe weather in " + country + " is " + weather_desc + " at " + weather_temp + " degrees Celsius."


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, "I don't understand what you mean. Type /help to see available commands.")


# Periodically send weather updates
def send_weather_updates():
    bot.send_message(-1001690185473, "The Weather Station bot is now alive!")
    # Fix the logic of this
    while True:
        update = SG_channel_Update()
        if update is None:
            print("Error! Weather update failed!")
            bot.send_message(-1001690185473, "Error! Weather update failed!")
        else:
            print("Weather update sent!")
            bot.send_message(-1001690185473, SG_channel_Update())

        time.sleep(60)  # Should be every hour/day but for Demo purposes, every minute


# Multiple threads

try:
    t = threading.Thread(target=send_weather_updates).start()
    bot.polling()
    # Catch SIGKILL
except KeyboardInterrupt or SystemExit:
    print("Bot stopped.")
    sys.exit()
