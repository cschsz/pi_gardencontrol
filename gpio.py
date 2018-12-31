#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

try:
    from RPi.GPIO import *
    imp = True
except ImportError:
    imp = False
    #----------------------------[setmode]
    def setmode(board):
        return

    #----------------------------[BOARD]
    def BOARD():
        return

    #----------------------------[setup]
    def setup(led, state):
        return

    #----------------------------[OUT]
    def OUT():
        return

    #----------------------------[IN]
    def IN():
        return

    #----------------------------[PUD_DOWN]
    def PUD_DOWN():
        return

    #----------------------------[LOW]
    def LOW():
        return 0

    #----------------------------[HIGH]
    def HIGH():
        return 1

    #----------------------------[output]
    def output(led, state):
        return

    #----------------------------[input]
    def input(pin):
        return 0

    #----------------------------[cleanup]
    def cleanup():
        return

pin_led = 12

#----------------------------[ledstatus]
def ledstatus(value):
    if value == 1:
        output(pin_led, HIGH)
    else:
        output(pin_led, LOW)
    return

#----------------------------[init]
def init():
    setmode(BOARD)
    setup(pin_led, OUT)

    ledstatus(0)
    return

#----------------------------[]
if __name__=='__main__':
    val = 0
    try:
        init()
        while True:
            time.sleep(1)
    except:
        cleanup()
