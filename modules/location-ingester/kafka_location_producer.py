import json
import logging
import os

from kafka import KafkaProducer
from typing import Dict
from json import dumps

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-ingester")

# Create the kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x:dumps(x).encode('utf-8')
    )


def store_location(location_data):
    logger.debug(f"Raw data to be sent to kafka: {location_data}")
    producer.send(TOPIC_NAME, location_data)
    producer.flush()
    logger.info(f"Published location data {location_data} to kafka successfully.")
