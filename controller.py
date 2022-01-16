from time import sleep
import os
import db
import db
from db import EVENT_HUMIDITY
from db import EVENT_TEMPERATURE
from db import EVENT_STARTUP
from db import EVENT_SHUTDOWN
import display
import RPi.GPIO as GPIO

#heatOutput = 23
heatOutput = 17

humidityOutput = 18 #nummer 18 op het shield
humiditySwitchTime = 0.1

high = GPIO.HIGH
low = GPIO.LOW


def setup():
    """setup GPIOs"""
    print('Setting up peripherals')
  #  GPIO.setmode(GPIO.BOARD)
    GPIO.setup(heatOutput, GPIO.OUT)
    GPIO.setup(humidityOutput, GPIO.OUT)
    sleep(1)
    deactivate_humidifier()


def destructor():
    deactivate_humidifier()
    deactivate_heatpad()
    GPIO.cleanup()


def activate_heatpad_timed(time):
    print("Activate heatpad")
    set_pin_to(heatOutput, low, time)
    db.writeEvent(EVENT_TEMPERATURE, 'on')


def deactivate_heatpad():
    print("Deactivate heatpad")
    set_pin_to(heatOutput, high)
    db.writeEvent(EVENT_TEMPERATURE, 'off')

def activate_heatpad():
    activate_heatpad_timed(1)

def activate_humidifier_timed(time):
    print("Activate humidifier")
    # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 1')
    activate_humidifier()
    sleep(time)
    deactivate_humidifier()

def activate_humidifier():
    set_pin_to(humidityOutput, high, humiditySwitchTime)
    set_pin_to(humidityOutput, low, humiditySwitchTime)
    db.writeEvent(EVENT_HUMIDITY, 'on')


def deactivate_humidifier():
    print("Deactivate humidifier")
    set_pin_to(humidityOutput, low, humiditySwitchTime)
    set_pin_to(humidityOutput, high, humiditySwitchTime)
    set_pin_to(humidityOutput, low, humiditySwitchTime)
    set_pin_to(humidityOutput, high, humiditySwitchTime)
    db.writeEvent(EVENT_HUMIDITY, 'off')
    # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 0')


def set_pin_to(pin, state, time=0):
    GPIO.output(pin, state)
    sleep(time)
