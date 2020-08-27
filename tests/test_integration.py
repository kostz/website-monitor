import multiprocessing
import os
from time import sleep

import pytest

import run_monitoring
import run_writer
from monitor.PostgresFactory import getPostgresDBCursorByFile


def safe_drop(db_cursor, stmt):
    db_cursor.execute(stmt)

#    try:
 #       db_cursor.execute(stmt)
#    except Exception:
#        pass


@pytest.fixture
def cleanup_database():
    db_cursor = getPostgresDBCursorByFile('test-config/config.yml')
    #safe_drop(db_cursor, 'drop table website_mon')
    #safe_drop(db_cursor, 'drop table website')


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

    ## wait until database tables are created
    sleep(10)

    yield

    monitoring.terminate()
    writer.terminate()


@pytest.mark.skip(reason="for now")
def test_integration(start_processes):
    db_cursor = getPostgresDBCursorByFile('tests/test-config/config.yml')

    cnt = 0
    while cnt < 10 and db_cursor.execute("select id from website where url='https://www.google.com'").fetchone() is not None:
        cnt += 1
        sleep(2)

    if cnt == 10:
        raise RuntimeError('website record was not found')

    website_id = db_cursor.execute("select id from website where url='https://www.google.com'").fetchone()[0]

    cnt = 0
    while cnt < 10 and db_cursor.execute("select * from website_mon where website_id={}".format(website_id)).fetchone() is not None:
        cnt += 1
        sleep(2)

    if cnt == 10:
        raise RuntimeError('website_mon record was not found')

    mon_id = db_cursor.execute("select min(id) from website_mon where website_id={}".format(website_id)).fetchone()

    assert db_cursor.execute("select * from website_mon where id={}".format(mon_id)).fetchone() == 1
