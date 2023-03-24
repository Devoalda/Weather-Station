# Weather-Station

# Installation:

```bash
pip install -r requirements.txt
```
# Usage
## Configuration
All configurations are stored in the `Config` folder. The `config.ini` file contains the configuration for the whole application.
```ini
[frontendServer]
IP = 127.0.0.1
Port = 5000

[backendServer]
IP = 127.0.0.1
Port = 12000

[SSL]
Cert = ../backend/SSL/certificate.pem
PrivateKey = ../backend/SSL/privatekey.pem

[TELEGRAM_BOT]
# Grab a token from @BotFather and paste it here
TOKEN = 
CHANNEL_ID = 

[FILE_DB]
# Path to the file database
FILE_PATH = ../backend/File_DB/payload_DB.json
```
Define all IPs and Ports for the Front and Backend Server. The SSL Cert and Private Key are used for the HTTPS connection. The Telegram Bot Token and Channel ID are used to send the data to a Telegram Channel. The File Path is the path to the file database.

The Telegram bot requires a API Token from `@BotFather` and a Channel ID. The Channel ID can be obtained by sending a message to the bot and head to the following link: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`. The Channel ID is the `chat` -> `id` field.

## Backend/Server
App is in the `backend` folder. To run it, the command:
```bash
python server.py
```
The server is required to be running for the application to work. The server is responsible for receiving the data from the weather station and storing it in the database. 
The server also sends the data to the Telegram Channel and hosts the telegram chatbot.

## Frontend
App is in the `flaskProject` folder. To run it, the command:
```bash
python app.py
```

## Client
The sample client is in the `backend` folder. To run it, the command:
```bash
python client.py
```
Both the flask application and the telegram bot uses the same client structure to send and receive data.

## Singapore Cache
The Singapore Cache is a cache that stores the weather data from the Singapore Weather API. The cache is used to reduce the number of API calls to the Singapore Weather API. The cache is stored in the `backend` folder. To run it, the command:
It starts with the backend server and runs in the background.

## Telegram Chatbot
The Telegram Chatbot is a chatbot that is used to retrieve the weather data from the database. The chatbot is stored in the `backend/TelegramBot` folder. To run it, the command:
```bash
python bot.py
```

# Service files
The service files are stored in the `services` folder. The service files are used to run the application as a service. The service files are used for the Raspberry Pi.
This requires `systemd` to be installed on the Raspberry Pi.

# Database

# JSON Database
The JSON Database is a file database that stores the weather data. The database is stored in the `backend/File_DB` folder. 

# MongoDB
installation for mongo in docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
docker run -d -p 27017:27017 -v ~/data:/data/db --name mongo mongo:bionic
```

how to start mongodb in raspberry pi
```bash
sudo docker start mongo
```

How to check if docker image mongodb is running:
```bash
sudo docker ps
```

In database.py, edit the variable "myclient" to insert the IP address of the raspberry pi which has the docker database installed in:
- For example if raspberry pi 1 has installed docker and run the container mongo and its IP address is 192.168.137.186, then replace the IP address in myclient.
```python
"myclient = pymongo.MongoClient("mongodb://192.168.100.100:27017/", connect=True, serverSelectionTimeoutMS=1000)" to
"myclient = pymongo.MongoClient("mongodb://192.168.137.192:27017/", connect=True, serverSelectionTimeoutMS=1000)"
```
