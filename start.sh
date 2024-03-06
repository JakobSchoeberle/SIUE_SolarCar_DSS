#!/bin/sh

cd /
cd home/SolarCar/SIUESolar_DriverSupportSystem
/usr/bin/tmux new-session -d -s DSS
/usr/bin/tmux send-keys -t DSS 'su SolarCar' C-m
/usr/bin/tmux send-keys -t DSS '/bin/python main.py' C-m
#/bin/python main.py
#sudo /bin/python main.py
cd /