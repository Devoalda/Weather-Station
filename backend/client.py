import json
from socket import *
from pprint import pprint
import ssl

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12000
# Client will use this function to get weather from server
def get_weather_from_Server(country):
    # Server Config
    # Change IP to your server IP

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('./SSL/certificate.pem')
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
    pprint(get_weather_from_Server("china"))


if __name__ == '__main__':
    main()
