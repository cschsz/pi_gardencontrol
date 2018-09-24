#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

#----------------------------[info]
def info(module, info):
    print(time.strftime("%Y-%m-%d %H:%M:%S") + ": [" + module + "] " + info)
    try:
        f = open("/var/log/pigc_{:s}.log".format(time.strftime("%Y-%m")),"a")
    except Exception:
        f = open("pigc_{:s}.log".format(time.strftime("%Y-%m")),"a")
    f.write(time.strftime("%Y-%m-%d %H:%M:%S") + ": [" + module + "] " + info + "\r\n")
    f.close()
    return

#----------------------------[line]
def line(line):
    try:
        f = open("/var/log/pigc_data.log","a")
    except Exception:
        f = open("pigc_data.log","a")
    f.write(time.strftime("%d.%m.%Y %H:%M") + ";" + line + "\r\n")
    f.close()
    return