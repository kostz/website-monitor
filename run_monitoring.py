import logging
import argparse
import yaml
import threading

from monitor.Checker import Checker
from monitor.KafkaFactory import getKafkaProducer
from utils import initLogger


def processItem(c: Checker, l: logging):
    l.info('started thread {}'.format(c.websiteUrl))
    while True:
        c.process()
        c.wait()


def runMonitoring(config_file_location):
    with open(config_file_location, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    logger = initLogger('monitor', level=config['log_level'])

    threads = []
    for w in config['websites']:
        x = threading.Thread(
            name='thread {}'.format(w['url']),
            target=processItem,
            args=(
                Checker(
                    website=w,
                    kafka_producer=getKafkaProducer(
                        kafka_connect=config['kafka_connect']
                    ),
                    kafka_topic=config['kafka_connect']['topic'],
                    default_interval=config['check_every_seconds_default']
                ),
                logger
            )
        )
        threads.append(x)
        x.start()


if __name__ == '__main__':
    a = argparse.ArgumentParser(description='website checker unit')
    a.add_argument('--config', help='config file name', default='config/config.yml')
    args = a.parse_args()
    runMonitoring(args.config)
