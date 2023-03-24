import json
from socket import *
import ssl
import configparser
import backend
from threading import Thread
import singapore_cache as singapore_cache

# Config
config = configparser.ConfigParser()
config.read('../Config/config.ini')
SERVER_PORT = int(config.get('backendServer', 'Port'))
CERT = config.get('SSL', 'Cert')
PRIVATEKEY = config.get('SSL', 'PrivateKey')

# Thread for client connection
def child(connectionSocket):
    # Receive country from client
    country = connectionSocket.recv(1024).decode()
    print("Received: " + country)
    # Get weather from backend
    weather_payload = backend.frontend_get_weather(country, "")
    # Send weather to client
    if weather_payload == None:
        # Send error to client if weather_payload is None
        connectionSocket.send("Error".encode())
    else:
        # Send weather to client
        connectionSocket.send(json.dumps(weather_payload).encode())
    connectionSocket.close()


def tcpServer(PORT, CERT, PRIVATEKEY):
    # TCP with TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT, PRIVATEKEY)

    # Create socket
    serverSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_side=True)
    # Bind socket to port
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
    # Safe exit
    except KeyboardInterrupt:
        print("Keyboard Interrupt, closing server...")
        serverSocket.close()
    except Exception as e:
        print(e)
        serverSocket.close()


def main():
    # Start singapore_cache thread
    singapore_cache.cache_Singapore()
    # Start TCP Server
    tcpServer(SERVER_PORT, CERT, PRIVATEKEY)


if __name__ == '__main__':
    main()
