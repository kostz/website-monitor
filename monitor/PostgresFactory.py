import os
import psycopg2
from psycopg2.extras import RealDictCursor


def createDatabaseObjectsSafe(cursor, logger):
    logger.debug('creating database object')
    cursor.execute(
        open(
            os.path.join(os.getcwd(), 'sql', 'create_database.sql'), 'r'
        ).read()
    )
    return True


def getPostgresDBCursor(postgres_uri):
    db = psycopg2.connect(postgres_uri)
    return db.cursor(cursor_factory=RealDictCursor)


def initDictionaries(db_cursor, websites, logger):
    websites_ids = dict()
    logger.debug('init dictionaries')
    for w in websites:
        w = w['url']
        logger.debug('processing {}'.format(w))
        db_cursor.execute("select id from website where url='{}'".format(w))
        res = db_cursor.fetchone()
        logger.debug(res)
        if res is None:
            db_cursor.execute("insert into website(url) values ('{}')".format(w))
            db_cursor.execute("select id from website where url='{}'".format(w))
            res = db_cursor.fetchone()
        websites_ids[w] = res
    return websites_ids
