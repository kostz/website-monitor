import json
import os
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


def _checkConnectItem(kafka_connect, item):
    if item not in kafka_connect or kafka_connect[item] is None:
        raise Exception('parameter {} is undefined or null'.format(item))


def _checkKafkaConnect(kafka_connect):
    _checkConnectItem(kafka_connect, 'uri')
    _checkConnectItem(kafka_connect, 'cafile')
    _checkConnectItem(kafka_connect, 'certfile')
    _checkConnectItem(kafka_connect, 'keyfile')
    _checkConnectItem(kafka_connect, 'topic')


def _createTopicIfNeeded(kafka_connect):
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_connect['uri'],
        security_protocol="SSL",
        ssl_cafile=os.path.join(os.getcwd(), kafka_connect['cafile']),
        ssl_certfile=os.path.join(os.getcwd(), kafka_connect['certfile']),
        ssl_keyfile=os.path.join(os.getcwd(), kafka_connect['keyfile'])
    )

    try:
        admin_client.create_topics(
            new_topics=[
                NewTopic(
                    name=kafka_connect['topic'],
                    num_partitions=1,
                    replication_factor=1
                )
            ],
            validate_only=False
        )
        admin_client.close()
    except TopicAlreadyExistsError:
        pass


def getKafkaProducer(**kwargs):
    kafka_connect = kwargs.get('kafka_connect')
    _checkKafkaConnect(kafka_connect)
    _createTopicIfNeeded(kafka_connect)

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
        security_protocol='SSL',
        group_id='database-writer',
        ssl_cafile=os.path.join(os.getcwd(), kafka_connect['cafile']),
        ssl_certfile=os.path.join(os.getcwd(), kafka_connect['certfile']),
        ssl_keyfile=os.path.join(os.getcwd(), kafka_connect['keyfile'])
    )

    return consumer
