#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import schedule

# own modules
import gpio as GPIO
import webserver
import log
import mail
import sensors

s_stoggle = True
s_scnt = 0

#----------------------------[status_led]
def status_led():
    global s_stoggle

    s_stoggle = not s_stoggle
    GPIO.ledgrn(s_stoggle)

#----------------------------[once_a_hour]
def once_a_hour():
    #read
    values = sensors.read()

    # format
    for i in range(len(values)):
        try:
            values[i] = "{:3.0f}".format(float(values[i]))
        except Exception:
            pass

    # log
    log.info("main", "once_a_hour")

    logline = ""
    for val in values:
        logline += str(val) + ";"
    logline = logline.replace(' ', '')
    log.line(logline)
    log.info("temp", logline)
    return

#----------------------------[main]
def main():
    # init
    GPIO.init()
    sensors.start()
    webserver.start()
    schedule.every().hour.at(':00').do(once_a_hour)

    # running
    while True:
        time.sleep(1)
        status_led()
        schedule.run_pending()

#----------------------------[]
if __name__=='__main__':
    try:
        log.info("main", "starting")
        mail.send("info", "Restarted")
        main()
    except:
        webserver.stop()
        time.sleep(0.5)
        sensors.stop()
        GPIO.cleanup()
        log.info("main", "exit")
