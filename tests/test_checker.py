import json
from unittest.mock import MagicMock, patch
from freezegun import freeze_time
from monitor.Checker import Checker
from utils import initLogger


def setup_module(module):
    logger = initLogger('monitor', level='DEBUG')


@freeze_time('2020-08-27 12:01:01')
@patch('monitor.Checker.requests.get')
def test_basic_positive_no_patterns(mock_get):
    mock_get.return_value.text = 'text'
    mock_get.return_value.status_code = 200
    mock_get.return_value.elapsed.microseconds=123

    producer_mock = MagicMock()
    producer_mock.send.return_value = True
    c = Checker(
        website={
            'url': 'https://www.website.com'
        },
        kafka_producer=producer_mock
    )
    c.process()
    assert {
        'time': '2020-08-27 12:01:01',
        'website': 'https://www.website.com',
        'http_status_code': 200,
        'elapsed': 123,
        'pattern_match': None
    } == json.loads(producer_mock.send.call_args[0][1])


@freeze_time('2020-08-27 12:01:01')
@patch('monitor.Checker.requests.get')
def test_basic_positive_w_patterns_not_match(mock_get):
    mock_get.return_value.text = 'header line \n line 2 abc aaa \n line 3 cbd'
    mock_get.return_value.status_code = 200
    mock_get.return_value.elapsed.microseconds=123

    producer_mock = MagicMock()
    producer_mock.send.return_value = True
    c = Checker(
        website={
            'url': 'https://www.website.com',
            'patterns': [
                '.*abc.*',
                '.*xyz.*'
            ]
        },
        kafka_producer=producer_mock
    )
    c.process()
    assert {
        'time': '2020-08-27 12:01:01',
        'website': 'https://www.website.com',
        'http_status_code': 200,
        'elapsed': 123,
        'pattern_match': False
    } == json.loads(producer_mock.send.call_args[0][1])


@freeze_time('2020-08-27 12:01:01')
@patch('monitor.Checker.requests.get')
def test_basic_positive_w_patterns_match(mock_get):
    mock_get.return_value.text = 'header line \n line 2 abc aaa \n line 3 xyz asd \n ending line'
    mock_get.return_value.status_code = 200
    mock_get.return_value.elapsed.microseconds=123

    producer_mock = MagicMock()
    producer_mock.send.return_value = True
    c = Checker(
        website={
            'url': 'https://www.website.com',
            'patterns': [
                '.*abc.*',
                '.*xyz.*'
            ]
        },
        kafka_producer=producer_mock
    )
    c.process()
    assert {
        'time': '2020-08-27 12:01:01',
        'website': 'https://www.website.com',
        'http_status_code': 200,
        'elapsed': 123,
        'pattern_match': True
    } == json.loads(producer_mock.send.call_args[0][1])
