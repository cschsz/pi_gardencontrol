#!/bin/bash
sudo cp -n pigc.ini /usr/local/etc
sudo mkdir /usr/local/bin/pigc
sudo cp *.py /usr/local/bin/pigc
sudo chmod +x /usr/local/bin/pigc/pigc.py
sudo chmod +x /usr/local/bin/pigc/pigc_sensors.py
sudo reboot
