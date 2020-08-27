import argparse
import logging
import threading
import yaml

from monitor.KafkaFactory import getKafkaConsumer
from monitor.PostgresFactory import getPostgresDBCursor, createDatabaseObjectsSafe, initDictionaries
from monitor.Writer import Writer
from utils import initLogger


def processItem(thread_id, writer: Writer, logger: logging):
    logger.info('started thread {}'.format(thread_id))
    while True:
        writer.process()


if __name__ == '__main__':
    a = argparse.ArgumentParser(description='website monitoring writer unit')
    a.add_argument('--config', help='config file name', default='config/config.yml')
    args = a.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    logger = initLogger('monitor', level=config['log_level'])

    # init database
    db = getPostgresDBCursor(config['target']['postgres_uri'])
    createDatabaseObjectsSafe(db, logger)
    websites_ids = initDictionaries(db, config['websites'], logger)

    threads = []
    thread_id = 0
    for w in config['websites']:
        x = threading.Thread(
            name='thread {}'.format(w['url']),
            target=processItem,
            args=(
                thread_id,
                Writer(
                    kafka_consumer=getKafkaConsumer(
                        kafka_connect=config['kafka_connect']
                    ),
                    db_cursor=getPostgresDBCursor(
                        config['target']['postgres_uri']
                    ),
                    websites_ids=websites_ids.copy()
                ),
                logger
            )
        )
        threads.append(x)
        x.start()
        thread_id += 1
