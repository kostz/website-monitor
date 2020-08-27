from unittest.mock import MagicMock

from monitor.Writer import Writer
from utils import initLogger


def setup_module(module):
    logger = initLogger('monitor', level='DEBUG')


def test_basic():
    message_mock = MagicMock()
    message_mock.value = {
        'time': '2020-08-27 12:01:01',
        'website': 'https://www.website.com',
        'http_status_code': 200,
        'elapsed': 123,
        'pattern_match': None
    }

    db_cursor_mock = MagicMock()
    db_cursor_mock.execute.return_value = True

    w = Writer(
        websites_ids={
          'https://www.website.com': 1
        },
        kafka_consumer=[
            message_mock
        ],
        db_cursor=db_cursor_mock
    )

    w.process()

    assert "insert into website_mon(request_time, website_id, elapsed, http_status_code, pattern_match)" \
           "  values(%s,%s,%s,%s,%s)" == db_cursor_mock.execute.call_args[0][0]

    assert ('2020-08-27 12:01:01',1,123,200,'null') == db_cursor_mock.execute.call_args[0][1]


def test_pattern_not_matched():
    message_mock = MagicMock()
    message_mock.value = {
        'time': '2020-08-27 12:01:01',
        'website': 'https://www.website.com',
        'http_status_code': 200,
        'elapsed': 123,
        'pattern_match': False
    }

    db_cursor_mock = MagicMock()
    db_cursor_mock.execute.return_value = True

    w = Writer(
        websites_ids={
          'https://www.website.com': 1
        },
        kafka_consumer=[
            message_mock
        ],
        db_cursor=db_cursor_mock
    )

    w.process()

    assert "insert into website_mon(request_time, website_id, elapsed, http_status_code, pattern_match)" \
           "  values(%s,%s,%s,%s,%s)" == db_cursor_mock.execute.call_args[0][0]

    assert ('2020-08-27 12:01:01', 1, 123, 200, False) == db_cursor_mock.execute.call_args[0][1]