import os

from kafka import KafkaConsumer
from kafka.errors import KafkaError
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
        store_location(message)

running = True

def basic_consume_loop(consumer, topics):
    try:
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.error(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n")
                elif msg.error():
                    logger.error(f"There is an error when process kafka: {msg.error()}")
            else:
                store_location(message)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False