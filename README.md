# pi_gardencontrol
measurement and control on raspberry pi

Key features of this project are:
* DHT22
* DS1820
* 433 MHz
* web access

Programm logging is found in /var/log/pigc_data.log and /var/log/pigc_[YEAR-MM].log

## Preparation
```
sudo apt-get update
sudo apt-get install python3-rpi.gpio
```

## Running
```
sudo python3 pigc.py
```

If already "installed" execute this before running from console:
```
ps -aux | grep pigc.py
sudo kill [pid]
```

**Running (DHT22)**
```
sudo python pigc_sensors.py
```
or
```
sudo python pigc_sensors.py &
```

## Hardware layout
http://rpi.science.uoit.ca/lab/gpio/
```
                   Status-LEDs
                    +---+---+
                    ^   |   ^
                   LED  |  LED
                    ^   |   ^
                   1k0  |  1k0
                    |   |   |
5V  5V  GND 8   10  12  GND 16  18  GND 22  24  26  28  GND 32  GND 36  38  40
3V3 3   5   7   GND 11  13  15  3V3 19  21  23  GND 27  29  31  33  35  37  GND
|           |   |               |    |          |
|        +--+   |               +4k7-+    +-----+
|        |  |   |               |    |    |
|       4k7 |   |               P1   P2   P4
|        |  |   |                  DHT22
+--------+  |   |
         |  |   |
        red | black
         |yellow|
   DS1820 (waterproof case)
```

## Installation
```
sudo ./install.sh
```

add in /etc/rc.local before the last line (exit 0):
```
/usr/local/bin/pigc/pigc.py &
/usr/local/bin/pigc/pigc_sensors.py &
```
