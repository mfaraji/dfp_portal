import time
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from django.conf import settings


logging.basicConfig()
logger = logging.getLogger("inspire.sqltime")
logger.setLevel(logging.DEBUG)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                        parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("Start Query: %s", statement)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                        parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logger.debug("Query Complete!")
    logger.debug("Total Time: %f", total)

def db_connect():
    return create_engine(settings.AWS_DATABASE_URL)



db = db_connect()