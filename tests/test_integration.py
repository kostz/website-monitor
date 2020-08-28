import multiprocessing
import os
from time import sleep

import pytest

import run_monitoring
import run_writer
from monitor.PostgresFactory import getPostgresDBCursorByFile


def safe_drop(db_cursor, stmt):
    try:
        db_cursor.execute(stmt)
    except Exception:
        pass


@pytest.fixture
def cleanup_database():
    db_cursor = getPostgresDBCursorByFile('test-config/config.yml')
    safe_drop(db_cursor, 'drop table website_mon')
    safe_drop(db_cursor, 'drop table website')


@pytest.fixture
def start_processes(cleanup_database):
    os.chdir(os.path.dirname(os.getcwd()))
    monitoring = multiprocessing.Process(
        target=run_monitoring.runMonitoring,
        args=('tests/test-config/config.yml',)
    )
    writer = multiprocessing.Process(
        target=run_writer.runWriter,
        args=('tests/test-config/config.yml',)
    )

    monitoring.start()
    writer.start()

    ## dirty wait until both sides is running and initialized
    sleep(10)

    yield

    monitoring.terminate()
    writer.terminate()


def fetch_records(c, stmt):
    c.execute(stmt)
    return c.fetchall()


@pytest.mark.skip(reason="its a bad idea to expose credentials to the public repo, and test is not stable because of NoBrokerException from Kafka side")
def test_integration(start_processes):
    db_cursor = getPostgresDBCursorByFile('tests/test-config/config.yml')
    cnt = 0

    while cnt < 10 and len(fetch_records(db_cursor, "select id from website where url='https://www.google.com'")) == 0:
        cnt += 1
        sleep(2)

    if cnt == 10:
        raise RuntimeError('website record was not found')

    website_id = fetch_records(db_cursor, "select id from website where url='https://www.google.com'")[0][0]

    cnt = 0
    while cnt < 10 and len(
            fetch_records(db_cursor, "select * from website_mon where website_id={}".format(website_id))) == 0:
        cnt += 1
        sleep(2)

    if cnt == 10:
        raise RuntimeError('website_mon record was not found')

    assert len(fetch_records(db_cursor, "select * from website_mon where website_id={}".format(website_id))) > 0
