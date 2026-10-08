import network
import socket
import machine
import requests
import json
import math
import time
from picozero import pico_led, LED
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
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    

def iss():
    """
    Get ISS data from open-notify.org
    """
    res = None
    longitude = None
    latitude = None
    
    try:
        res = requests.get(url='http://api.open-notify.org/iss-now.json')
        iss_details = json.loads(res.text)
        longitude = iss_details['iss_position']['longitude']
        latitude = iss_details['iss_position']['latitude']
    
    except OSError as e:
        print(f'Network error: {e}')
        
    except ValueError as e:
        print(f'Invalid JSON: {e}')
        
    finally:
        if res is not None:
            res.close()
    
    number = None
    
    try:
        res = requests.get(url='http://api.open-notify.org/astros.json')
        iss_crew = json.loads(res.text)
        number = iss_crew['number']
    
    except OSError as e:
        print(f'Network error: {e}')
        
    except ValueError as e:
        print(f'Invalid JSON: {e}')
        
    finally:
        if res is not None:
            res.close()
            
    if longitude is not None:        
        print(f'ISS longitude is {longitude} and latitude is {latitude}')

    if number is not None:
        print(f'ISS crew number is {number}')
    
    if longitude is not None and number is not None:
        return True, float(latitude), float(longitude), float(number)
    else:
        return False, None, None, None

def geolocation():
    """
    Get IP Geolocation from ip-api.com
    """
    res = None
    longitude = None
    latitude = None
    
    try:
        res = requests.get(url='http://ip-api.com/json/?fields=lat,lon')
        geo_details = json.loads(res.text)
        longitude = geo_details['lon']
        latitude = geo_details['lat']
        
    except OSError as e:
        print(f'Network error: {e}')
        
    except ValueError as e:
        print(f'Invalid JSON: {e}')
        
    finally:
        if res is not None:
            res.close()
            
    if longitude is not None:
        print(f'My longitude is {longitude} and latitude is {latitude}')
        return True, float(latitude), float(longitude)
    else:
        return False, None, None

def iss_visibility(iss_lat, iss_lon, my_lat, my_lon, max_distance_km=1000):
    """
    Returns:
        visible      - True if ISS distance <= max distance
        
    All lat/lon values are in degrees.
    """

    R = 6371.0  # Earth radius in km

    # Convert to radians
    lat1 = math.radians(my_lat)
    lon1 = math.radians(my_lon)
    lat2 = math.radians(iss_lat)
    lon2 = math.radians(iss_lon)

    # Earth-centred angular separation
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1) *
        math.cos(lat2) *
        math.sin(dlon / 2 ) ** 2
    )
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R * c
    
    delay = 300
    
    if distance_km <= max_distance_km:
        delay = 10
    elif distance_km <= (max_distance_km * 3):
        delay = 60
    
    visible = (distance_km <= max_distance_km)
    
    return visible, delay

def alive():
    """
    Blink on board led
    """
    pico_led.on()
    time.sleep(0.5)
    pico_led.off()
    time.sleep(1.0)
    pico_led.on()
    time.sleep(0.5)
    pico_led.off()
    
def blink_led(number=1):
    """
    Blinks GPIO port 13 'number' of times
    """
    i=0
    while i < number:
        antenna.on()
        time.sleep(0.5)
        antenna.off()
        time.sleep(0.5)
        i = i + 1

antenna = LED(13) # Use GP13

try:
    connect()
    
except KeyboardInterrupt:
    machine.reset()

go, my_lat, my_lon = geolocation()

while go:
    alive()
    status, iss_lat, iss_lon, num = iss()
    
    if status:
        visible, delay = iss_visibility(iss_lat, iss_lon, my_lat, my_lon)
        
        if visible:
            print('Lookup! ISS visible.')
            blink_led(num)
        else:
            print('ISS is not currently visible.')
            alive()
            
        time.sleep(delay)
