import logging


class Writer:

    def __init__(self, **kwargs):
        self.db_cursor = kwargs.get('db_cursor')
        self.websites_ids = kwargs.get('websites_ids')
        self.consumer = kwargs.get('kafka_consumer')
        self.logger = logging.getLogger('monitor.writer')

        self.logger.debug(self.websites_ids)

    def process(self):
        for message in self.consumer:
            message = message.value
            self.logger.info('message received {}'.format(message))
            self.db_cursor.execute(
                "insert into website_mon(request_time, website_id, elapsed, http_status_code, pattern_match)"
                "  values(%s,%s,%s,%s,%s)",
                (
                    message['time'],
                    self.websites_ids[message['website']],
                    message['elapsed'],
                    message['http_status_code'],
                    message['pattern_match'],
                )
            )



