import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

import pygeohash as pgh

bucket="Nova"

def SendOrionBMS1(message, write_api):
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    .field("PackInstVoltage", message['PackInstVoltage'])
    .field("PackCurrent", message['PackCurrent']*0.1)
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)
  #time.sleep(1) # separate points by 1 second'

def SendOrionBMS2(message, write_api):
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    .field("LowTemperature", message['LowTemperature'])
    .field("HighTemperature", message['HighTemperature'])
    .field("SimulatedSOC", message['SimulatedSOC'])
    .field("MaxCellNumber", message['MaxCellNumber'])
    .field("PackCCL", message['PackCCL']) # Charge Current Limit
    .field("PackDCL", message['PackDCL']) # Discharge Current Limit
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendOrionBMS3(message, write_api):
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    .field("PackAmphours", message['PackAmphours'])
    .field("OpenPackVoltageint", message['OpenPackVoltage'])
    .field("PackResistance", message['PackResistance'])
    .field("PackSOCint", message['PackSOC'])
    #.field("CustomFlag1", message['CustomFlag1'])
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendOrionBMS4(message, write_api):
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    #.field("RelayState", message['RelayState'])
    #.field("CustomFlag2", message['CustomFlag2'])
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendGPS(message, write_api):

  gpshash = pgh.encode(message['latitude'], message['longitude'])

  point = (
  Point("GPS")
  #.tag("tagname1", "tagvalue1")
  .field("latitude", message['latitude'])
  .field("longitude", message['longitude'])
  .field("Geohash", gpshash)
  .field("satellites", message['satellites'])
  #.field("timestamp_utc", message['timestamp_utc'])
  .field("altitude_m", message['altitude_m'])
  .field("speed_knots", message['speed_knots'])
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendGPS1(message, write_api):
  point = (
  Point("GPS")
  #.tag("tagname1", "tagvalue1")
  .field("Geohash", message)
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendInstrumentationPageNGM(message, write_api):
  point = (
    Point("NGM")
    #.tag("tagname1", "tagvalue1")
    .field("AM_velocity", message['AM_velocity'])
    .field("AM_supplyV", message['AM_supplyV'])
    .field("AM_supplyI", message['AM_supplyI'])
    .field("AM_baseplateT", message['AM_baseplateT'])
    .field("AM_ambientT", message['AM_ambientT'])
    .field("AM_motorT", message['AM_motorT'])
    .field("AM_SOC", message['AM_SOC'])
    .field("AM_thr", message['AM_thr'])
    .field("AM_rgn", message['AM_rgn'])
    .field("SV_desiredphaseI", message['SV_desiredphaseI'])
    .field("SV_desiredspd", message['SV_desiredspd'])
    .field("SV_targetphaseI", message['SV_targetphaseI'])

    # SV_drivestate
    .field("BIT_initialized", message['SV_drivestate']['BIT_initialized'])
    .field("BIT_charging", message['SV_drivestate']['BIT_charging'])
    .field("BIT_motornotready", message['SV_drivestate']['BIT_motornotready'])
    .field("BIT_interlock", message['SV_drivestate']['BIT_interlock'])
    .field("BIT_enabled", message['SV_drivestate']['BIT_enabled'])
    .field("BIT_active", message['SV_drivestate']['BIT_active'])
    .field("BIT_standby", message['SV_drivestate']['BIT_standby'])
    .field("BIT_transition", message['SV_drivestate']['BIT_transition'])
    .field("BIT_INdisable", message['SV_drivestate']['BIT_INdisable'])
    .field("BIT_limiting", message['SV_drivestate']['BIT_limiting'])
    .field("BIT_spdctrl", message['SV_drivestate']['BIT_spdctrl'])
    .field("BIT_reverse", message['SV_drivestate']['BIT_reverse'])
    .field("DriveState", message['SV_drivestate']['DriveState'])
    
    .field("SV_fault1latch", message['SV_fault1latch'])

    # SV_fault1
    .field("FA1_stuckthr", message['SV_fault1']['FA1_stuckthr'])
    .field("FA1_PDPINT", message['SV_fault1']['FA1_PDPINT'])
    .field("FA1_lostcomm", message['SV_fault1']['FA1_lostcomm'])
    .field("FA1_SCItimeoutzero", message['SV_fault1']['FA1_SCItimeoutzero'])

    # SV_fault2
    .field("FA2_rgnexcite", message['SV_fault2']['FA2_rgnexcite'])
    .field("FA2_threxcite", message['SV_fault2']['FA2_threxcite'])
    .field("FA2_SOClost", message['SV_fault2']['FA2_SOClost'])
    .field("FA2_SCInoise", message['SV_fault2']['FA2_SCInoise'])
    .field("FA2_supplyI", message['SV_fault2']['FA2_supplyI'])

    .field("SV_fault3", message['SV_fault3'])

    .field("SV_thrlimit", message['SV_thrlimit'])
    .field("SV_rgnlimit", message['SV_rgnlimit'])
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)

def SendOrionBMSCells(message, write_api):
  if (message['Checksum'] == True):
    point = (
      Point("OrionBMS")
      #.tag("tagname1", "tagvalue1")
      .field("Cell" + str(message['Cell ID']) + "_InstantVoltage", message['InstantVoltage'])
      .field("Cell" + str(message['Cell ID']) + "_InternalResistance", message['InternalResistance'])
      .field("Cell" + str(message['Cell ID']) + "_OpenVoltage", message['OpenVoltage'])
    )

    write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)
  else:
    print("Cell Checksum Failed")
