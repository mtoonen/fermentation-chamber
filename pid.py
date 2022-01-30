import time
import board
import datetime
import adafruit_dht
import db
from db import EVENT_STARTUP
from db import EVENT_SHUTDOWN
import display
import controller
import ds18b20 as probe

target_temperature = 30
target_humidity = 70

sensor = adafruit_dht.DHT11(board.D5)
sensor_back = adafruit_dht.DHT11(board.D27)

timeHeat = 1
timeHumidifier = 5

temperature_threshold = 1
temperature_threshold_env = 6
humidityThreshold = 1

loopTimeout = 20


def setupMain():
    db.setup()
    display.setup(target_temperature, target_humidity)
    display.set_phase("Initializing")
    controller.setup()


def main():
    setupMain()
    db.write_event(EVENT_STARTUP, '_')
    display.set_phase("Initialization complete")
    warmup(0)
    loop()


def warmup(warmup_time):
    display.set_phase("Warmup {} s".format(warmup_time))
    db.write_event(db.EVENT_WARMUP, 'warmuptime: {}, targettemp: {}, targethumidity: {}'
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
    controller.deactivate_humidifier()
    controller.deactivate_heatpad()


def write_sensors(sensor_readings):
    average_temp = average(sensor_readings, "temperature")
    average_humidity = average(sensor_readings, "humidity")
    print("Current temp average: {}, main: {}, achter: {}"
          .format(average_temp, sensor_readings["temperature"][0], sensor_readings["temperature"][1]))
    print("Current humidity average: {}, main: {}, achter: {}"
          .format(average_humidity, sensor_readings["humidity"][0], sensor_readings["humidity"][1]))

    display.set_sensors(average_temp, average_humidity)

    db.write_sensors(sensor_readings)


def get_sensor_readings():
    readings = {"temperature": [], "humidity": []}

    try:
        readings["temperature"].append(sensor.temperature)
        readings["humidity"].append(sensor.humidity)
    except RuntimeError as error:
        readings["temperature"].append(None)
        readings["humidity"].append(None)

    try:
        readings["temperature"].append(sensor_back.temperature)
        readings["humidity"].append(sensor_back.humidity)
    except RuntimeError as error:
        readings["temperature"].append(None)
        readings["humidity"].append(None)


    return readings


def loop():
    display.set_phase("Mainloop")
    try:
        while True:
            temperature_probe = probe.read_temp()
            db.write_probe(temperature_probe)
            display.set_probe(temperature_probe)
            print("Probe temperature: {}".format(temperature_probe))

            try:
                readings = get_sensor_readings()

                write_sensors(readings)
                temperature = average(readings, "temperature")
                humidity = min_of_list(readings, "humidity")

                if temperature_probe - temperature_threshold > target_temperature:
                    controller.deactivate_heatpad()
                else:
                    if temperature - temperature_threshold_env > target_temperature:
                        controller.deactivate_heatpad()
                    else:
                        controller.activate_heatpad()

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


def average(readings, key):
    filtered = [number for number in readings[key] if number is not None]
    if len(filtered) == 0:
        raise RuntimeError("errored on reading sensors")
    return sum(filtered) / len(filtered)


def min_of_list(readings, key):
    filtered = [number for number in readings[key] if number is not None]
    if len(filtered) == 0:
        raise RuntimeError("errored on reading sensors")
    return min(filtered)


def destructor():
    display.destructor()
    controller.destructor()
    db.write_event(EVENT_SHUTDOWN, '_')
    db.destructor()


def exit_handler():
    print('Cleanup')
    destructor()


if __name__ == '__main__':
    main()
