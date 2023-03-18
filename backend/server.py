import json
from socket import *
from pprint import pprint
import ssl
from threading import Thread

import configparser

import backend

def child(connectionSocket):
    country = connectionSocket.recv(1024).decode()
    print("Received: " + country)
    weather_payload = backend.frontend_get_weather(country, "")
    if weather_payload == None:
        connectionSocket.send("Error".encode())
    else:
        connectionSocket.send(json.dumps(weather_payload).encode())
    connectionSocket.close()

def tcpServer(PORT, CERT, PRIVATEKEY):
    # serverSocket = socket(AF_INET, SOCK_STREAM)
    # TCP with TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT, PRIVATEKEY)

    serverSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_side=True)
    serverSocket.bind(('', PORT))

    try:
        # TCP Server
        serverSocket.listen(1)
        print('The server is ready to receive')
        while True:
            connectionSocket, addr = serverSocket.accept()
            print('Connected to :', addr[0], ':', addr[1])
            t = Thread(target=child, args=(connectionSocket,))
            t.start()
    except KeyboardInterrupt:
        print("Keyboard Interrupt, closing server...")
        serverSocket.close()
    except Exception as e:
        print(e)
        serverSocket.close()

def main():
    config = configparser.ConfigParser()
    config.read('../Config/config.ini')
    SERVER_PORT = int(config.get('backendServer', 'Port'))
    CERT = config.get('SSL', 'Cert')
    PRIVATEKEY = config.get('SSL', 'PrivateKey')

    tcpServer(SERVER_PORT, CERT, PRIVATEKEY)
    # Cache Singapore weather
    # Supposed to run together but its not
    #try:
    #    singapore_cache.cache_Singapore()
    #except Exception as e:
    #    print(e)


if __name__ == '__main__':
    main()