import threading
import adafruit_gps
import time
import board
import serial

import WebSockets as Web
import Common as Global


VideoEnable = False

if (VideoEnable == True):
    Videothread = threading.Thread(target=Web.Video_Server)
    Videothread.start()

Datathread = threading.Thread(target=Web.Data_Server)
Datathread.start()

# ---- Input ----s

Value1 = 140
Global.Values[0] = Value1
Value2 = 180
Global.Values[1] = Value2

uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()
while True:

    gps.update()

    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print('Waiting for fix...')
            continue
        print('=' * 40)  # Print a separator line.
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        Global.Values[0] = str(gps.latitude)
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        Global.Values[1] = str(gps.longitude)