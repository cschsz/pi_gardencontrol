#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import socket
import time
import log

array = [ "?", "?", "?", "?", "?", "?", "?"] # dht-temp, dht-humi, ds1820(1), ds1820(2), ds1820(3), boden, regen
smaa = [ "?", "?"]
sflag = False

#----------------------------[read]
def read():
    return array+smaa

#----------------------------[sensordata]
def sensordata(data):
    global array
    global smaa
    log.info("sensor", "received: " + data)
    try:
        if data[:5] == "pigc;":
            xarr = data.split(";")
            if len(xarr) == 8:
                xarr.remove("pigc")
                array = list(xarr)
        if data[:4] == "sma;":
            xarr = data.split(";")
            if len(xarr) == 3:
                xarr.remove("sma")
                smaa = list(xarr)
    except Exception:
        pass
    return

#----------------------------[sensorthread]
def sensorthread():
    log.info("sensor", "init")
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 4712))
            s.settimeout(1)
            s.listen(1)
            break
        except Exception:
            if sflag == True:
                log.info("sensor", "stop")
                return
            log.info("sensor", "init error")
            time.sleep(5)

    log.info("sensor", "started")
    while True:
        try:
            conn, addr = s.accept()
            conn.settimeout(1)
            #log.info("sensor", "connection accepted " + str(addr))
            while True:
                try:
                    data = str(conn.recv(128), "utf-8")
                    if not data: break
                    sensordata(data)
                except socket.timeout:
                    if sflag == True:
                        conn.close()
                        s.close()
                        log.info("sensor", "stop")
                        return
            conn.close()
            #log.info("sensor", "connection closed")
        except socket.timeout:
            if sflag == True:
                s.close()
                log.info("sensor", "stop")
                return
    return

#----------------------------[stop]
def stop():
    global sflag
    sflag = 1
    return

#----------------------------[start]
def start():
    thread = threading.Thread(target=sensorthread, args=[])
    thread.start()
    return
