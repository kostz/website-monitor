import json
import time
import logging

import requests
from datetime import datetime

import re


class Checker:
    websiteUrl = ''
    producer = None
    patterns = []

    def __init__(self, **kwargs):
        self.websiteConfig = kwargs.get('website')
        self.producer = kwargs.get('kafka_producer')
        self.topic = kwargs.get('kafka_topic')
        self.logger = logging.getLogger('monitor.checker')

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
        else:
            self.patterns = []

    def getTimestamp(self):
        return str(datetime.now())

    def process(self):
        self.logger.debug('--- processing start')
        now = self.getTimestamp()

        try:
            r = requests.get(self.websiteUrl)
            self.logger.debug('get request done: {}'.format(r.status_code))
            self.logger.debug('patterns {}'.format(self.patterns))
            self.logger.debug('config {}'.format(self.websiteConfig))
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
        except Exception:
            msg = {
                'time': now,
                'website': self.websiteUrl,
                'http_status_code': 999,
                'elapsed': 0,
                'pattern_match': None
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
