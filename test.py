from time import sleep
import os
import RPi.GPIO as GPIO

heatOutput = 12
debug = True

humidityOutput = 12
humiditySwitchTime = 0.1

high = GPIO.HIGH
low = GPIO.LOW

def setup():
    """setup GPIOs"""
    print('Setting up peripherals')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(heatOutput, GPIO.OUT)
    GPIO.setup(humidityOutput, GPIO.OUT)
    sleep(1)
    deactivateHumidifier()




def activateHeatpad(time):
    print("Activate heatpad")
    setPinTo(heatOutput, low, time)


def deactivateHeatpad():
    print("Deactivate heatpad")
    setPinTo(heatOutput, high)


def activateHumidifier(time):
    print("Activate humidifier")
    # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 1')
    setPinTo(humidityOutput,high, humiditySwitchTime)
    setPinTo(humidityOutput,  low, humiditySwitchTime)
    sleep(time)
    deactivateHumidifier()

def deactivateHumidifier():
    print("Deactivate humidifier")
    setPinTo(humidityOutput, low, humiditySwitchTime)
    setPinTo(humidityOutput, high, humiditySwitchTime)
    setPinTo(humidityOutput, low, humiditySwitchTime)
    setPinTo(humidityOutput, high, humiditySwitchTime)
    # os.system('sudo hub-ctrl -b 001 -d 002 -P 2 -p 0')

def setPinTo(pin, state, time=0):
    GPIO.output(pin, state)
    sleep(time)