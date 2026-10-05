import network
import socket
import machine
import requests
import json
import math
import time
from picozero import pico_led
from secrets import ssid, password


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
    return float(latitude), float(longitude)

def geolocation():
    """
    Get IP Geolocation from ip-api.com
    """
    res = requests.get(url='http://ip-api.com/json/?fields=lat,lon')
    geo_details = json.loads(res.text)
    longitude = geo_details['lon']
    latitude = geo_details['lat']
    print(f'My longitude is {longitude} and latitude is {latitude}')
    return float(latitude), float(longitude)

def iss_visibility(iss_lat, iss_lon, my_lat, my_lon,
                   iss_alt_km=420.0, min_elevation_deg=10.0):
    """
    Returns:
        visible      - True if ISS elevation >= minimum elevation
        distance_km  - Approximate straight-line distance to ISS
        elevation_deg - ISS elevation above local horizon

    All lat/lon values are in degrees.
    """

    R = 6371.0  # Earth radius in km

    # Convert to radians
    lat1 = math.radians(my_lat)
    lon1 = math.radians(my_lon)
    lat2 = math.radians(iss_lat)
    lon2 = math.radians(iss_lon)

    # Earth-centred angular separation
    dlon = lon2 - lon1

    cos_c = (
        math.sin(lat1) * math.sin(lat2) +
        math.cos(lat1) * math.cos(lat2) * math.cos(dlon)
    )

    # Clamp for floating-point safety
    cos_c = max(-1.0, min(1.0, cos_c))

    central_angle = math.acos(cos_c)

    # Distance from Earth's centre
    r_iss = R + iss_alt_km

    # Straight-line distance from observer to ISS
    distance_km = math.sqrt(
        R * R +
        r_iss * r_iss -
        2.0 * R * r_iss * math.cos(central_angle)
    )

    # Elevation angle
    numerator = r_iss * math.cos(central_angle) - R
    denominator = r_iss * math.sin(central_angle)

    elevation_rad = math.atan2(numerator, denominator)
    elevation_deg = math.degrees(elevation_rad)

    visible = elevation_deg >= min_elevation_deg

    return visible

def blink_led():
    pico_led.on()
    time.sleep(1)
    pico_led.off()
    time.sleep(1)
    
try:
    connect()
    my_lat, my_lon = geolocation()
    
except KeyboardInterrupt:
    machine.reset()
    
while True:
    try:
        iss_lat, iss_lon = iss()
        visible = iss_visibility(iss_lat, iss_lon, my_lat, my_lon)
        
        if visible:
            print("Lookup! ISS is above 10 degrees.")
            blink_led()
        else:
            print("ISS is not currently visible.")
        
        time.sleep(600)
        
    except KeyboardInterrupt:
        machine.reset()
