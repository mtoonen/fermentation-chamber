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

current_state_humidity = True
current_state_heatmat = False


def setup():
    """setup GPIOs"""
    print('Setting up peripherals')
    GPIO.setup(heatOutput, GPIO.OUT)
    GPIO.setup(humidityOutput, GPIO.OUT)
    sleep(2)
    deactivate_humidifier()


def destructor():
   # deactivate_humidifier()
    deactivate_heatpad()
    GPIO.cleanup()


def activate_heatpad_timed(time):
    global current_state_heatmat
    if not current_state_heatmat:
        print("Activate heatpad")
        display.set_output_heatmat(True)
        current_state_heatmat = True
        db.write_event(EVENT_TEMPERATURE, 'on')
        set_pin_to(heatOutput, low, time)
        deactivate_heatpad()


def deactivate_heatpad():
    global current_state_heatmat
    if current_state_heatmat:
        print("Deactivate heatpad")
        set_pin_to(heatOutput, high)
        display.set_output_heatmat(False)
        db.write_event(EVENT_TEMPERATURE, 'off')
        current_state_heatmat = False


def activate_heatpad():
    global current_state_heatmat
    if not current_state_heatmat:
        print("Activate heatpad")
        display.set_output_heatmat(True)
        set_pin_to(heatOutput, low)
        db.write_event(EVENT_TEMPERATURE, 'on')
        current_state_heatmat = True


def activate_humidifier_timed(time):
    global current_state_humidity
    if not current_state_humidity:
        # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 1')
        activate_humidifier()
        current_state_humidity = True
        sleep(time)
        deactivate_humidifier()


def activate_humidifier():
    global current_state_humidity
    if not current_state_humidity:
        print("Activate humidifier")
        set_pin_to(humidityOutput, high, humiditySwitchTime)
        set_pin_to(humidityOutput, low, humiditySwitchTime)
        display.set_output_humidifier(True)
        db.write_event(EVENT_HUMIDITY, 'on')
        current_state_humidity = True


def deactivate_humidifier():
    global current_state_humidity
    if current_state_humidity:
        print("Deactivate humidifier")
        set_pin_to(humidityOutput, low, humiditySwitchTime)
        set_pin_to(humidityOutput, high, humiditySwitchTime)
        set_pin_to(humidityOutput, low, humiditySwitchTime)
        set_pin_to(humidityOutput, high, humiditySwitchTime)
        display.set_output_humidifier(False)
        db.write_event(EVENT_HUMIDITY, 'off')
        current_state_humidity = False
        # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 0')


def set_pin_to(pin, state, time=0):
    GPIO.output(pin, state)
    sleep(time)
