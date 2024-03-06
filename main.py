import threading
import adafruit_gps
import time
import board
import json
import serial
import cantact
import cantools
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

import ngm as NGM
import influxdatabase as indb

GPSEnable = True
CANEnable = True
NGMEnable = False

# ------ DB Initialization ------
load_dotenv()
token = os.getenv('Influx_Token')
org = "SIUE Solar Racing Team"
url = os.getenv('Influx_URL')

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ------ NGM Initialization ------
if(NGMEnable == True):
    loop = 1 # loop for slowing down the contact with ngm
    ser = serial.Serial('/dev/ttyUSB0')
    ser.baudrate = 19200

# ------ GPS Initialization ------
if(GPSEnable == True):
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)
    gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    gps.send_command(b'PMTK220,1000')
    last_print = time.monotonic()

# ------ CAN BUS Initialization ------
if(CANEnable == True):
    intf = cantact.Interface() # create the interface
    intf.set_bitrate(0, 500000) # set the CAN bitrate
    intf.set_enabled(0, True) # enable channel 0
    intf.start() # start the interface

    db = cantools.database.load_file('dbc/BMS.dbc') # Loads the CAN Database


# ------------ Main Loop ------------
while True:
    # ------------ NGM ------------
    if(NGMEnable == True):
        loop = loop + 1
        if loop == 1000:
            ser.write(b'1**?\r')
            line = ser.readline()
            line = ser.readline()
            ngmmessage = NGM.InstrumentationPageDecode(line)
            try:
                indb.SendInstrumentationPageNGM(ngmmessage, write_api)
            except:
                print("Failed to send to server")
            #print(json.dumps(NGM.InstrumentationPageDecode(line)))
            loop = 1
    
    # ------------ GPS ------------
    if(GPSEnable == True):
        gps.update()
        current = time.monotonic()

        if current - last_print >= 1.0:
            last_print = current
            if not gps.has_fix:
                print('Waiting for fix...')
                continue
            print('=' * 40)  # Print a separator line.
            print('Latitude: {0:.6f} degrees'.format(gps.latitude))

            print('Longitude: {0:.6f} degrees'.format(gps.longitude))

            gps.speed_knots

            gpsOutput = {
            'latitude': gps.latitude,
            'longitude': gps.longitude,
            'satellites':gps.satellites,
            #'timestamp_utc':gps.timestamp_utc,
            'altitude_m':gps.altitude_m,
            'speed_knots':gps.speed_knots
            }
            try:
                indb.SendGPS(gpsOutput, write_api)
            except:
                print("Failed to send to server")
            #gpshash = pgh.encode(gps.latitude, gps.longitude)
            #indb.SendGPS1(gpshash, write_api)
            print("Sent")

    # ------------ CAN BUS ------------
    if(CANEnable == True):
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
                    #print(message)
                    if (hex(f['id']) == '0x3b'):
                        try:
                            indb.SendOrionBMS1(message, write_api)
                        except:
                            print("Failed to send to server")
                    elif (hex(f['id']) == '0x3cb'):
                        try:
                            indb.SendOrionBMS2(message, write_api)
                        except:
                            print("Failed to send to server")
                    elif (hex(f['id']) == '0x6b2'):
                        try:
                            indb.SendOrionBMS3(message, write_api)
                        except:
                            print("Failed to send to server")
                    #elif (hex(f['id']) == '0x3c'):
                        #indb.SendOrionBMS4(message, write_api)

        except KeyboardInterrupt:
            # ctrl-c pressed, close the interface
            intf.stop()
            break

    #print("Heartbeat")

