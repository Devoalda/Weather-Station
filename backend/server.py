import json
from socket import *
from pprint import pprint
import ssl
from threading import Thread
import backend
# import singapore_cache

certificate = "./SSL/certificate.pem"
privatekey = "./SSL/privatekey.pem"
def child(connectionSocket):
    country = connectionSocket.recv(1024).decode()
    print("Received: " + country)
    weather_payload = backend.frontend_get_weather(country, "", "")
    connectionSocket.send(json.dumps(weather_payload).encode())
    connectionSocket.close()

def tcpServer():
    serverPort = 12000
    # serverSocket = socket(AF_INET, SOCK_STREAM)
    # TCP with TLS
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certificate, privatekey)

    serverSocket = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_side=True)
    serverSocket.bind(('', serverPort))

    try:
        # TCP Server
        serverSocket.listen(1)
        print('The server is ready to receive')
        while True:
            connectionSocket, addr = serverSocket.accept()
            print('Connected to :', addr[0], ':', addr[1])
            t = Thread(target=child, args=(connectionSocket,))
            t.start()
    except Exception as e:
        print(e)
        serverSocket.close()

def main():
    tcpServer()
    # Cache Singapore weather
    # Supposed to run together but its not
    #try:
    #    singapore_cache.cache_Singapore()
    #except Exception as e:
    #    print(e)


if __name__ == '__main__':
    main()