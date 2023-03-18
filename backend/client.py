import json
from socket import *
from pprint import pprint
import ssl
import configparser

# Client will use this function to get weather from server
def get_weather_from_Server(country):
    # Server Config
    config = configparser.ConfigParser()
    config.read('../Config/config.ini')
    SERVER_PORT = int(config.get('backendServer', 'Port'))
    SERVER_IP = config.get('backendServer', 'IP')
    CERT = config.get('SSL', 'Cert')
    # Change IP to your server IP

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT)
    context.check_hostname = False

    clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=SERVER_IP)
    clientSocket.connect((SERVER_IP, SERVER_PORT))

    clientSocket.send(country.encode())
    buffer = 10240
    data = clientSocket.recv(buffer).decode()
    if data == "Error":
        payload = None
    else:
        payload = json.JSONDecoder().decode(data)
    clientSocket.close()
    return payload

def main():
    pprint(get_weather_from_Server("Singapore"))


if __name__ == '__main__':
    main()
