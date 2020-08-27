import os
import psycopg2
import yaml


def createDatabaseObjectsSafe(cursor, logger):
    logger.debug('creating database object')
    cursor.execute(
        open(
            os.path.join(os.getcwd(), 'sql', 'create_database.sql'), 'r'
        ).read()
    )
    return True


def getPostgresDB(postgres_uri):
    db = psycopg2.connect(postgres_uri)
    db.set_session(autocommit=True)
    return db


def getPostgresDBCursor(postgres_uri):
    db = getPostgresDB(postgres_uri)
    return db.cursor()


def getPostgresDBCursorByFile(config_file_location):
    with open(config_file_location, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    return getPostgresDBCursor(config['target']['postgres_uri'])


def initDictionaries(db_cursor, websites, logger):
    websites_ids = dict()
    logger.debug('init dictionaries')
    for w in websites:
        w = w['url']
        logger.debug('processing {}'.format(w))
        db_cursor.execute("select id from website where url=%s", (w,))
        res = db_cursor.fetchone()
        logger.debug(res)
        if res is None:
            db_cursor.execute("insert into website(url) values (%s)", (w,))
            db_cursor.execute("select id from website where url=%s", (w,))
            res = db_cursor.fetchone()
        websites_ids[w] = res[0]
    return websites_ids
