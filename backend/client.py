import json
from socket import *
from pprint import pprint
import ssl

# Client will use this function to get weather from server
def get_weather_from_Server(country):
    # Server Config
    serverIP = "127.0.0.1"
    serverPort = 12000

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('./SSL/certificate.pem')
    context.check_hostname = False

    clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=serverIP)
    clientSocket.connect((serverIP, serverPort))

    clientSocket.send(country.encode())
    buffer = 2048
    payload = json.JSONDecoder().decode(clientSocket.recv(buffer).decode())
    clientSocket.close()
    return payload

def main():
    pprint(get_weather_from_Server("Vietnam"))


if __name__ == '__main__':
    main()
