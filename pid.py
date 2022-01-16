import time
import board
import datetime
import adafruit_dht
import db
from db import EVENT_STARTUP
from db import EVENT_SHUTDOWN
import display
import controller

target_temperature = 30
target_humidity = 70

sensor = adafruit_dht.DHT22(board.D5)

timeHeat = 1
timeHumidifier = 10

temperature_threshold = 1
humidityThreshold = 1

loopTimeout = 20


def setupMain():
    db.setup()
    display.setup(target_temperature, target_humidity)
    display.set_phase("Initializing")
    controller.setup()


def main():
    setupMain()
    db.writeEvent(EVENT_STARTUP, '_')
    display.set_phase("Initialization complete")
    warmup(0)
    loop()


def warmup(warmup_time):
    display.set_phase("Warmup {} s".format(warmup_time))
    db.writeEvent(db.EVENT_WARMUP, 'warmuptime: {}, targettemp: {}, targethumidity: {}'
                  .format(warmup_time, target_temperature, target_humidity))
    controller.activate_humidifier()
    controller.activate_heatpad()

    start = datetime.datetime.now().timestamp()

    current_time = datetime.datetime.now()
    while current_time.timestamp() - start < warmup_time:
        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
            if temperature > target_temperature:
                controller.deactivate_heatpad()
                break;
            if humidity > target_humidity:
                controller.deactivate_humidifier()
            else:
                controller.activate_humidifier()

            write_sensors(humidity, temperature)
            time.sleep(10)
            current_time = datetime.datetime.now()

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue


def write_sensors(humidity, temperature):
    print("Current temp {}".format(temperature))
    print("Current humidity {}".format(humidity))

    display.set_sensors(temperature, humidity);

    db.writeSensors(humidity, temperature)


def loop():
    display.set_phase("Mainloop")
    try:
        while True:

            try:
                # Print the values to the serial port
                temperature = sensor.temperature
                humidity = sensor.humidity

                write_sensors(humidity, temperature)
                if target_temperature - temperature > temperature_threshold:
                    controller.activate_heatpad()
                else:
                    controller.deactivate_heatpad()

                if target_humidity - humidity > humidityThreshold:
                    controller.activate_humidifier_timed(timeHumidifier)

            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                sensor.exit()
                raise error

            time.sleep(loopTimeout)
    finally:
        exit_handler()


def destructor():
    display.destructor()
    controller.destructor()
    db.writeEvent(EVENT_SHUTDOWN, '_')
    db.destructor()


def exit_handler():
    print('Cleanup')
    destructor()


if __name__ == '__main__':
    main()
