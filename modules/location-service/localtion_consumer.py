import os

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from location_database import store_location
from json import loads
import logging

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-location-consumer")

# Create the kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

running = True

def basic_consume_loop(consumer):
    try:
        while running:
            for msg in consumer:
                logger.info(f"{msg}")
                if msg is None: continue

                if msg is not None:
                    store_location(msg.value)

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

basic_consume_loop(consumer)

def shutdown():
    running = False