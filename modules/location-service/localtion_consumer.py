import os

from kafka import KafkaConsumer
from location_database import store_location
from json import loads

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

# Create the kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

while True:
    for message in consumer:
        location_data = message.value.decode('utf-8')
        store_location(location_data)
