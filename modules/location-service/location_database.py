import json
import logging
import os
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
from schemas import LocationSchema
from typing import Dict

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-service")


def store_location(location):
    try:
        location_dict = json.loads(location)
    except:
        logger.warning(f"There is an error: non-dictionary payload detected: {location}")
        return

    validation_result: Dict = LocationSchema().validate(location_dict)

    if validation_result:
        logger.warning(f"There is an error: data format in payload: {location}, reason: {validation_result}")
        return

    if location_dict["longitude"] > 180 or location_dict["longitude"] < -180:
        logger.error(f"There is an error: longitude format in payload: {location}, reason: longitude out of range")


    if location_dict["latitude"] > 90 or location_dict["longitude"] < -90:
        logger.error(f"There is an error: latitude format in payload: {location}, reason: latitude out of range")

    with psycopg2.connect(
        database = DB_NAME,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    ) as conn:
        person_id = int(location_dict["person_id"])
        with conn.cursor() as cursor:
            try:
                query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}))".format(person_id, location_dict["latitude"], location_dict["longitude"])
                cursor.execute(query)
            except OperationalError as e:
                logger.error(f"Unable to save location data to the database. reason: {e}")