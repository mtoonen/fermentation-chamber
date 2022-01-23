from config import db
import psycopg2
import datetime

connection: any

EVENT_STARTUP = 'startup'
EVENT_WARMUP = 'warmup'
EVENT_SHUTDOWN = 'shutdown'
EVENT_HUMIDITY = 'humidifier'
EVENT_TEMPERATURE = 'heatmat'


def setup():
    try:
        #db.get('user')
        global connection
        connection = psycopg2.connect(user=db.get('user'),
                                      password=db.get('password'),
                                      host=db.get('host'),
                                      port=db.get('port'),
                                      database=db.get('database'))
        print("connection made")
    except (Exception, psycopg2.Error) as error:
        print("Failed to create connection", error)
        raise error


def destructor():
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")


def writeSensors(sensor_readings):
    try:
        global connection
        cursor = connection.cursor()

        postgres_insert_query = """INSERT INTO measurements (humidity, temperature, humidity_achter, 
        temperature_achter, timestamp) VALUES (%s,%s,%s,%s,%s) """
        record_to_insert = (sensor_readings["humidity"][0], sensor_readings["temperature"][0],
                            sensor_readings["humidity"][1], sensor_readings["temperature"][1],
                            datetime.datetime.now())
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)
    finally:
        if cursor:
            cursor.close()


def writeEvent(event, action):
    cursor = None;
    try:
        global connection
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO events (eventtype, action, timestamp) VALUES (%s,%s,%s)"""
        record_to_insert = (event, action, datetime.datetime.now())
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)
    finally:
        if cursor:
            cursor.close()
