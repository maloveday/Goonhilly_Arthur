import network
import socket
import machine
import requests
from time import sleep
from picozero import pico_led
from secrets import ssid, password


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


try:
    ip = connect()
    res = requests.get(url='http://api.open-notify.org/iss-now.json')
    print(res.text)
    res = requests.get(url='http://api.open-notify.org/astros.json')
    print(res.text)
except KeyboardInterrupt:
    machine.reset()