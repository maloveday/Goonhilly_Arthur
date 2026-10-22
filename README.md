# ISS_Arthur
An ISS (International Space Station) location notifier using a raspberry PI and 3d paper model of the Arthur Satellite dish at Goonhilly Earth Station in the UK.

Developed by Alec Short
for www.apollo50.co.uk

# Adapted for Raspberry Pi Pico W

A Raspberry Pi Pico W project that tracks the International Space Station (ISS) and flashes the onboard LED when the ISS is passing near IP geolocation.

When the ISS is within the configured distance threshold, the LED flashes once for each astronaut currently aboard the ISS.

## What It Does

The Pico W:

- Connects to Wi-Fi.
- Retrieves the latitude and longitude of your public IP address 
- Retrieves the current ISS latitude and longitude.
- Retrieves the current number of people aboard the ISS.
- Calculates the distance between the ISS ground position and my location.
- Determines whether the ISS is within a configured overhead distance.
- Flashes the LED once for each astronaut aboard the ISS when the ISS is nearby.

For example, if there are 7 astronauts aboard:

```text
FLASH FLASH FLASH FLASH FLASH FLASH FLASH
```

## Hardware

- Raspberry Pi Pico W
- LED and 220 ohm to 330 ohm resistor in series connect between Pin 13 and GND 
- Wi-Fi connection
- USB power supply

No additional hardware is required.

## Software

The project uses MicroPython and the Pico W networking capability.

Typical modules used include:

```python
import network
import requests
import time
import math
from picozero import pico_led, LED
from secrets import ssid, password
```

## Geolocation Data


## ISS Data

ISS position data is retrieved from:

```text
http://api.open-notify.org/iss-now.json
```

The API returns the current latitude and longitude of the ISS.

Example:

```json
{
    "iss_position": {
        "longitude": "2.6048",
        "latitude": "47.3104"
    }
}
```

The project also retrieves the current ISS crew count from the Open Notify people API.

## Determining When the ISS Is Overhead

The program calculates the great-circle distance between:

- My latitude and longitude.
- The current ISS sub-satellite latitude and longitude.

The Haversine formula is used to calculate the approximate surface distance.

The project currently considers the ISS to be overhead when its ground position is within:

```text
1000 km
```

of my location.

This threshold can be changed in the program.

## Polling Interval

The ISS travels at approximately 7.7 km/s and completes an orbit of Earth roughly every 93 minutes.

Because an overhead pass may only last a few minutes, the ISS position should be checked relatively frequently.

A polling interval of around:

```text
30–60 seconds
```

is recommended when accurate pass detection is required.

Long polling intervals, such as 10 minutes, can completely miss a pass.

## LED Behaviour

When the ISS is outside the configured range:

```text
LED OFF
```

When the ISS enters the configured range, the Pico retrieves the number of astronauts aboard and flashes the LED that many times.

For example:

```text
ISS crew number is 7
ISS is overhead!

LED flashes 7 times
```

The LED therefore provides a simple physical indication of both:

1. An ISS pass near the observer.
2. The number of people currently living aboard the station.

## Automatic Startup

The program should be stored on the Pico as:

```text
main.py
```

MicroPython automatically runs `main.py` whenever the Pico starts or resets.

Alternatively, the main application can be stored in another file:

```text
iss_tracker.py
```

with a small `main.py` launcher:

```python
import iss_tracker

iss_tracker.run()
```

## Network Errors

Because the project relies on Internet APIs, occasional network failures are expected.

For example:

```text
OSError: [Errno 103] ECONNABORTED
```

These should be handled so that a temporary Wi-Fi or API failure does not stop the tracker.

Example:

```python
try:
    response = requests.get(url)

except OSError as error:
    print("Network error:", error)
```

The program can then wait and retry rather than terminating.

## Example Output

```text
Waiting for connection...
Connected on 192.168.0.72

My longitude is -4.1329 and latitude is 50.368

ISS longitude is 24.4913 and latitude is 46.7629
ISS crew number is 7
ISS is not currently overhead.

ISS longitude is 2.6048 and latitude is 47.3104
ISS crew number is 7

Look up! ISS overhead!

Flashing LED 7 times
```

## Possible Future Improvements

Potential improvements include:

- Detect whether the ISS is approaching or moving away.
- Increase the polling rate when the ISS gets closer.
- Predict the next ISS pass.
- Display the current distance to the ISS.
- Display ISS elevation above the horizon.
- Add an OLED display.
- Use different LED flash patterns for approaching, overhead, and departing passes.
- Store pass statistics.
- Add a buzzer when the ISS passes overhead.

## Purpose

This is a simple educational project combining:

- MicroPython
- Raspberry Pi Pico W
- Wi-Fi
- REST APIs
- Latitude/longitude calculations
- Basic orbital tracking
- Physical LED output

The result is a small standalone device that quietly monitors the ISS and comes to life whenever the space station passes nearby.
