import time, threading, backend


def cache_Singapore():
    print(time.ctime())
    # Get weather from API every 1 day
    backend.get_weather_from_WTTRIN("Singapore")
    threading.Timer(86400, cache_Singapore).start()


print("Starting Singapore Cache")
cache_Singapore()
