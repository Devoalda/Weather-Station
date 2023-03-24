import json
from socket import *
from pprint import pprint
import ssl
import configparser

# Sample client that requires server to be running

# Client will use this function to get weather from server
def get_weather_from_Server(country):
    # Server Config
    config = configparser.ConfigParser()
    config.read('../Config/config.ini')
    SERVER_PORT = int(config.get('backendServer', 'Port'))
    SERVER_IP = config.get('backendServer', 'IP')
    CERT = config.get('SSL', 'Cert')

    # Establish connection with server through TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CERT)
    context.check_hostname = False

    clientSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname=SERVER_IP)
    clientSocket.connect((SERVER_IP, SERVER_PORT))

    # Send country to server
    clientSocket.send(country.encode())
    buffer = 10240
    # Receive weather from server
    data = clientSocket.recv(buffer).decode()
    if data == "Error":
        payload = None
    else:
        payload = json.JSONDecoder().decode(data)
    clientSocket.close()
    return payload

def main():
    # Get weather from server through client (Uncomment to test)
    # pprint(get_weather_from_Server("Singapore"))
    pass


if __name__ == '__main__':
    main()
