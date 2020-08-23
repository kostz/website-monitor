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

        if 'patterns' in self.websiteConfig['patterns']:
            for p in self.websiteConfig['patterns']:
                self.patterns.append(
                    re.compile(p, re.IGNORECASE)
                )

    def process(self):
        now = datetime.now()
        r = requests.get(self.websiteUrl)

        patterns_matched = True
        for p in self.patterns:
            if not p.match(r.text):
                patterns_matched = False

        msg = {
            'time': now,
            'website': self.websiteUrl,
            'http_status_code': r.status_code,
            'elapsed': r.elapsed,
            'patternsMatched': patterns_matched
        }

        self.logger.debug(msg)
        self.producer.send(
            self.topic,
            json.dumps(msg).encode('utf-8')
        )

    def wait(self):
        time.sleep(self.sleepTime)
