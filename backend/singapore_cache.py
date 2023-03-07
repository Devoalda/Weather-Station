import time, threading, backend

def cache_Singapore():
    try:
        backend.get_weather_from_WTTRIN("Singapore")
        print(time.ctime())
        # Get weather from API every 1 day
        threading.Timer(86400, cache_Singapore).start()
    except Exception as e:
        print(e)
        threading.Timer(86400, cache_Singapore).start()
