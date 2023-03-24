import time, threading, backend

# This is a script that runs in the background to cache Singapore's weather

def cache_Singapore():
    print(time.ctime())
    # Get weather from API every 1 day
    backend.get_weather_from_WTTRIN("Singapore")
    # 86400 seconds = 1 day
    threading.Timer(86400, cache_Singapore).start()


print("Starting Singapore Cache")
cache_Singapore()
