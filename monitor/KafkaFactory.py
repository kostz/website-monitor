import json
import os
from kafka import KafkaProducer, KafkaConsumer


def _checkConnectItem(kafka_connect, item):
    if item not in kafka_connect or kafka_connect[item] is None:
        raise Exception('parameter {} is undefined or null'.format(item))


def _checkKafkaConnect(kafka_connect):
    _checkConnectItem(kafka_connect, 'uri')
    _checkConnectItem(kafka_connect, 'cafile')
    _checkConnectItem(kafka_connect, 'certfile')
    _checkConnectItem(kafka_connect, 'keyfile')
    _checkConnectItem(kafka_connect, 'topic')


def getKafkaProducer(**kwargs):
    kafka_connect = kwargs.get('kafka_connect')
    _checkKafkaConnect(kafka_connect)

    producer = KafkaProducer(
        bootstrap_servers=kafka_connect['uri'],
        security_protocol="SSL",
        ssl_cafile=os.path.join(os.getcwd(), kafka_connect['cafile']),
        ssl_certfile=os.path.join(os.getcwd(), kafka_connect['certfile']),
        ssl_keyfile=os.path.join(os.getcwd(), kafka_connect['keyfile'])
    )

    return producer


def getKafkaConsumer(**kwargs):
    kafka_connect = kwargs.get('kafka_connect')
    _checkKafkaConnect(kafka_connect)

    consumer = KafkaConsumer(
        kafka_connect['topic'],
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        bootstrap_servers=kafka_connect['uri'],
        security_protocol="SSL",
        ssl_cafile=os.path.join(os.getcwd(), kafka_connect['cafile']),
        ssl_certfile=os.path.join(os.getcwd(), kafka_connect['certfile']),
        ssl_keyfile=os.path.join(os.getcwd(), kafka_connect['keyfile'])
    )

    return consumer
