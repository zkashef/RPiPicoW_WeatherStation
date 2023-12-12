# record temperature & humidity measurements from shtc3 sensor
# publish to Adafruit IO feeds using Raspberry Pi Pico W

import time
import board
import adafruit_shtc3
import busio
from secrets import secrets
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
import ssl
import socketpool
import wifi
import adafruit_requests

# connect to wifi
wifi.radio.connect(secrets['ssid'], secrets['password'])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# connect to Adafruit IO HTTP API
io = IO_HTTP(secrets['aio_username'], secrets['aio_key'], requests)
print("connected to io")

# initalize temperature & humidity Adafruit IO feeds
temperature_feed = io.get_feed("plants.temperature")
humidity_feed = io.get_feed("plants.humidity")

# initalize shtc3 humidity & temp sensor with I2C bus
i2c = busio.I2C(sda=board.GP2,scl=board.GP3) 
shtc3 = adafruit_shtc3.SHTC3(i2c)

while True:
    # gather temp & humidity measurements from shtc3 sensor
    temperature, humidity = shtc3.measurements

    # send temp & humidity measurements to Adafruit IO
    io.send_data(temperature_feed['key'], temperature)
    io.send_data(humidity_feed['key'], humidity)

    print("sent data to io")
    print("temperature: ", temperature)
    print("humidity: ", humidity)
    print("")

    time.sleep(60)