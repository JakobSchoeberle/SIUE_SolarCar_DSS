# Introduction
This repository holds the code for the SIUE Solar Car's Onboard Telemetry System.

# Telemetry System Architecture
The SIUE Solar Racing Team's Telemetry System is designed to be very flexible and modular. Using a common time series database and a common database viewer the system is able to scale to the needs of the team. Currently the system consists of two components the server and the onboard collection device. The system relys on the use of a onboard hotspot to upload data to the server that is hosted back on the SIUE Campus.

# Onboard Architecture
We are using a Raspberry Pi as our device that is connected to the CAN bus. It also has a GPS attached to one of the UART Channels. There are also plans to intergrate a backup radio that would use LoRa UART radio to communicate with the car. This would required the team to have a separate radio and terminal. The main method for data transmission to the server is though Wi-Fi. The car will have its own hotspot that will provide the car with its own network for the Raspberry Pi to connect to using it's onboard Wi-Fi module.

# Hardware
- Raspberry Pi 3B+
- USB CAN Bus Module
- Adafruit Ultimate GPS
- SparkFun LoRaSerial (Not integrated yet)
- Hostspot (Separate device)

# Setup Process
(Work in progress)