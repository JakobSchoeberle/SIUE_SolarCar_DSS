import threading
import adafruit_gps
import time
import board
import json
import serial
import cantact
import cantools

import WebSockets as Web
import Common as Global


VideoEnable = False

if (VideoEnable == True):
    Videothread = threading.Thread(target=Web.Video_Server)
    Videothread.start()

#Datathread = threading.Thread(target=Web.Data_Server)
#Datathread.start()

# ---- Input ----

Value1 = 140
Global.Values[0] = Value1
Value2 = 180
Global.Values[1] = Value2

uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()

# create the interface
intf = cantact.Interface()

# set the CAN bitrate
intf.set_bitrate(0, 500000)

# enable channel 0
intf.set_enabled(0, True)

# start the interface
intf.start()

db = cantools.database.load_file('dbc/BMS.dbc')

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

    try:
        # wait for frame with 10 ms timeout
        f = intf.recv(10)
        if f != None:
            hex_strings = [hex(f['data'][0]), hex(f['data'][1]), hex(f['data'][2]), hex(f['data'][3]), hex(f['data'][4]), hex(f['data'][5]), hex(f['data'][6]), hex(f['data'][7])]
            # Concatenate the hexadecimal strings together into one string
            combined_hex = ''.join(hex_string[2:].zfill(2) for hex_string in hex_strings)
            # Convert the combined hexadecimal string into bytes
            AllOfTheHex = bytes.fromhex(combined_hex)

            if hex(f['id']) == '0x3b' or hex(f['id']) == '0x3cb' or hex(f['id']) == '0x6b2' or hex(f['id']) == '0x3c': 
                message = db.decode_message(f['id'], AllOfTheHex)
                print(message)
            

    except KeyboardInterrupt:
        # ctrl-c pressed, close the interface
        intf.stop()
        break

