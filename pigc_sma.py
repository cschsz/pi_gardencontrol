#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import asyncio
import aiohttp
import pysma
import socket
import configparser

# own modules
import log

values = [ "?", "?"]

#----------------------------[interpret_values]
def interpret_values(sensors):
    for sen in sensors:
        if sen.name == "grid_power":
            values[0] = str(sen.value)
        if sen.name == "daily_yield":
            values[1] = str(sen.value)

        if sen.value is None:
            print("{:>25}".format(sen.name))
        else:
            print("{:>25}{:>15} {}".format(sen.name, str(sen.value), sen.unit))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 4712))
    except Exception:
        log.info("sma", "pigc: connection failed")
        return
    data = "sma;{:s};{:s}".format(values[0], values[1])
    s.send(data.encode("utf-8"))
    s.close()
    return

#----------------------------[get_values]
async def get_values(url, user, password):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        sma = pysma.SMA(session, url, password=password, group=user)

        try:
            await sma.new_session()
        except pysma.exceptions.SmaAuthenticationException:
            log.info("sma", "Authentication failed!")
            return
        except pysma.exceptions.SmaConnectionException:
            log.info("sma", "Unable to connect to device at %s", url)
            return

        try:
            sensors = await sma.get_sensors()
            device_info = await sma.device_info()

            for name, value in device_info.items():
                print("{:>15}{:>25}".format(name, value))

            for sensor in sensors:
                sensor.enabled = True

            await sma.read(sensors)
            interpret_values(sensors)
            log.info("sma", "Closing Session...")
            await sma.close_session()
        except:
            log.info("sma", "Exception...")
            await sma.close_session()

#----------------------------[mainloop]
async def mainloop(url, user, password):
    while True:
        await get_values(url, user, password)
        time.sleep(30)

#----------------------------[main]
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('/usr/local/etc/pigc.ini')
    try:
        user  = config["SMA"]["USER"]
        pasw  = config["SMA"]["PASSWORD"]
        url   = config["SMA"]["URL"]
        try:
            log.info("sma", "starting")
            asyncio.run(mainloop(url, user, pasw))
        except:
            log.info("sma", "exit")    
    except KeyError:
        log.info("sma", "pigc.ini not filled")
