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

pin_red = 12
pin_grn = 16

#----------------------------[ledred]
def ledred(value):
    if value == 1:
        output(pin_red, HIGH)
    else:
        output(pin_red, LOW)
    return

#----------------------------[ledgrn]
def ledgrn(value):
    if value == 1:
        output(pin_grn, HIGH)
    else:
        output(pin_grn, LOW)
    return

#----------------------------[init]
def init():
    setmode(BOARD)
    setup(pin_red, OUT)
    setup(pin_grn, OUT)

    ledred(0)
    ledgrn(0)
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
