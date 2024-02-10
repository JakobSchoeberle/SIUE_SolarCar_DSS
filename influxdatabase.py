import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

bucket="Nova"

def SendBMS(message, write_api):
  point = (
    Point("OrionBMS")
    #.tag("tagname1", "tagvalue1")
    .field("Voltage", message['PackInstVoltage'] * 0.1)
  )

  write_api.write(bucket=bucket, org="SIUE Solar Racing Team", record=point)
  time.sleep(1) # separate points by 1 second'