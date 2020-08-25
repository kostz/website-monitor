import json
import time
from datetime import datetime
from logging import Logger

import requests
import re


class Checker:
    websiteUrl = ''
    producer = None
    logger: Logger
    patterns = []

    def __init__(self, **kwargs):
        self.websiteConfig = kwargs.get('website')
        self.producer = kwargs.get('kafka_producer')
        self.topic = kwargs.get('kafka_topic')
        self.logger = kwargs.get('logger')

        self.logger.debug(self.websiteConfig)

        self.websiteUrl = self.websiteConfig['url']

        if 'check_every_seconds' in self.websiteConfig:
            self.sleepTime = self.websiteConfig['check_every_seconds']
        else:
            self.sleepTime = kwargs.get('default_interval')
        self.logger.info('sleep time {}'.format(self.sleepTime))
        if 'patterns' in self.websiteConfig:
            for p in self.websiteConfig['patterns']:
                self.patterns.append(p)

    def process(self):
        self.logger.debug('--- processing start')
        now = str(datetime.now())
        r = requests.get(self.websiteUrl)
        self.logger.debug('get request done: {}'.format(r.status_code))
        if len(self.patterns) == 0:
            patterns_matched = None
        else:
            patterns_matched = True
            for p in self.patterns:
                if len(re.findall(p, r.text)) == 0:
                    patterns_matched = False
        self.logger.debug('pattern match: {}'.format(patterns_matched))
        msg = {
            'time': now,
            'website': self.websiteUrl,
            'http_status_code': r.status_code,
            'elapsed': r.elapsed.microseconds,
            'pattern_match': patterns_matched
        }

        self.logger.info('sending message {}'.format(msg))
        self.producer.send(
            self.topic,
            json.dumps(msg).encode('utf-8')
        )
        self.logger.debug('message sent')
        self.logger.debug('--- processing end')

    def wait(self):
        self.logger.debug('sleep for {}'.format(self.sleepTime))
        time.sleep(self.sleepTime)
