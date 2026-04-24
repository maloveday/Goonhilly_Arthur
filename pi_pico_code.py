import network
import socket
import machine
import requests
import json
from time import sleep
from picozero import pico_led
from secrets import ssid, password
from math import radians, sin, cos, sqrt, atan2


def connect():
    """
    Connect to WLAN
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    

def iss():
    """
    Get ISS data from open-notify.org
    """
    res = requests.get(url='http://api.open-notify.org/iss-now.json')
    iss_details = json.loads(res.text)
    longitude = iss_details['iss_position']['longitude']
    latitude = iss_details['iss_position']['latitude']
    res = requests.get(url='http://api.open-notify.org/astros.json')
    iss_crew = json.loads(res.text)
    number = iss_crew['number']
    print(f'ISS longitude is {longitude} and latitude is {latitude}')
    print(f'ISS crew number is {number}')
    return longitude, latitude, number


try:
    connect()
    iss()
except KeyboardInterrupt:
    machine.reset()