import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from django.core.cache import cache

from django.conf import settings
from inspire.logger import logger

def generate_aws_report(communities=[], interests=[], metrics=[]):
    summary = None
    market_research = None
    offers = None

    if 'n_sent' in metrics or 'n_opened' in metrics or 'n_clicked' in metrics or 'n_clicks' in metrics:
        summary = get_activity_summary(communities=communities)

    if 'market_research' in metrics:
        market_research = fetch_market_research(interests=interests, communities=communities)

    if 'offers' in metrics:
        offers = fetch_offers(interests=interests, communities=communities)
    logger.debug(interests)

    return summary, market_research, offers

def db_connect():
    return create_engine(settings.AWS_DATABASE_URL)

def get_activity_summary(communities=[]):
    logger.info('Fetching Acitivity Summary')
    db = db_connect()
    Session = sessionmaker(bind=db)
    session = Session()
    today = datetime.datetime.today().date()
    last_month = today - datetime.timedelta(days=38)
    meta = MetaData()
    summary = Table('asat_summary', meta, autoload=True, autoload_with=db)
    logger.debug('ASAT Summary from %s to %s', today, last_month)
    if not communities:
        query = (select([summary.c.group_id.label('community_id'), func.sum(summary.c.n_sent).label('n_sent'), func.sum(summary.c.n_opened).label('n_opened'), \
            func.sum(summary.c.n_clicked).label('n_clicked'), func.sum(summary.c.n_clicks).label('n_clicks')])\
            .where(summary.c.d_sent >= last_month).group_by(summary.c.group_id))
        logger.debug("AS %s", str(query))
    else:
        query = (select([summary.c.group_id.label('community_id'), func.sum(summary.c.n_sent).label('n_sent'), func.sum(summary.c.n_opened).label('n_opened'), \
            func.sum(summary.c.n_clicked).label('n_clicked'), func.sum(summary.c.n_clicks).label('n_clicks')])\
            .where(and_(summary.c.d_sent >= last_month, summary.c.group_id.in_(communities))).group_by(summary.c.group_id))
    logger.debug('ASAT query: %s', str(query))
    result = session.execute(query)
    logger.info('Acitivity Summary: %s' % result.rowcount)
    return result

def list_interests():
    db = db_connect()
    query = "select interests.i_id, conditions.name from interests join conditions on interests.i_ref_id = conditions.condition_id"
    result = db.engine.execute(query)
    return result


def filter_result(iterator, position=None, objs=[]):
    if objs:
        return [item for item in iterator if item[position] in objs]
    else:
        return [item for item in iterator]

def fetch_market_research(interests=[], communities=[]):
    logger.info('Fetching market research')
    db = db_connect()
    sql_roles_users_interests = """
        SELECT roles.r_obj_id AS community_id, count(roles.r_obj_id) AS market_research FROM roles JOIN 
        (SELECT interests_query.uid FROM
        (SELECT interests.uid AS uid 
        FROM interests 
        WHERE interests.i_ref_id in {0}) AS interests_query JOIN (SELECT users_preferences.uid AS uid 
        FROM users_preferences JOIN users ON users_preferences.uid = users.uid
        WHERE users_preferences.pref_id = 'msg_market_research' AND users_preferences.value = 1 AND users.country = 'US') 
        AS users_prefs ON interests_query.uid = users_prefs.uid) AS users_interests ON roles.r_uid =  users_interests.uid GROUP BY roles.r_obj_id
    """

    sql_roles_users_no_interests = """
        SELECT roles.r_obj_id AS community_id, count(roles.r_obj_id) AS offers FROM roles JOIN 
        (SELECT users_preferences.uid AS uid 
        FROM users_preferences JOIN users ON users_preferences.uid = users.uid
        WHERE users_preferences.pref_id = 'msg_market_research' AND users_preferences.value = 1 AND users.country = 'US') AS users_prefs ON roles.r_uid =  users_prefs.uid GROUP BY roles.r_obj_id
    """
    if interests:
        ids_list = '(%s)' % ','.join(interests)
        query = sql_roles_users_interests.format(ids_list)
    else:
        query = sql_roles_users_no_interests
    logger.debug('Query to fetch Market research: %s', query)
    result = db.engine.execute(query)
    logger.info('Market Research: %s' % result.rowcount)
    return result
    
def fetch_offers(interests=[], communities=[]):
    logger.info('Fetching Offers')
    db = db_connect()
    sql_roles_users_with_interests = """
        SELECT roles.r_obj_id AS community_id, count(roles.r_obj_id) AS offers FROM roles JOIN 
        (SELECT interests_query.uid FROM
        (SELECT interests.uid AS uid 
        FROM interests 
        WHERE interests.i_ref_id in {0}) AS interests_query JOIN (SELECT users_preferences.uid AS uid 
        FROM users_preferences JOIN users ON users_preferences.uid = users.uid
        WHERE users_preferences.pref_id = 'msg_offers' AND users_preferences.value = 1 AND users.country = 'US') 
        AS users_prefs ON interests_query.uid = users_prefs.uid) AS users_interests ON roles.r_uid =  users_interests.uid GROUP BY roles.r_obj_id
    """

    sql_roles_users_no_interests = """
       SELECT roles.r_obj_id AS community_id, count(roles.r_obj_id) AS offers FROM roles JOIN 
        (SELECT users_preferences.uid AS uid 
        FROM users_preferences JOIN users ON users_preferences.uid = users.uid
        WHERE users_preferences.pref_id = 'msg_offers' AND users_preferences.value = 1 AND users.country = 'US') AS users_prefs ON roles.r_uid =  users_prefs.uid GROUP BY roles.r_obj_id
    """
    query = None

    if interests:
        ids_list = '(%s)' % ','.join(interests)
        query = sql_roles_users_with_interests.format(ids_list)
    else:
        query = sql_roles_users_no_interests
    logger.debug('Query to fetch offers: %s', query)
    result = db.engine.execute(query)
    logger.info('Offers: %s' % result.rowcount)
    return result


def update_us_users_ratio():
    logger.debug('Calculating the ratio of user users')
    db = db_connect()
    query = "select roles.r_obj_id, sum(case when users.country = 'US' and users.status = 4 then 1 else 0 end) / count(roles.r_obj_id) from users join roles on users.uid = roles.r_uid where users.status = 4 group by roles.r_obj_id;"
    result = db.engine.execute(query)
    for row in result:
        if row[0] not in (None, 0):
            logger.debug('setting us_ratio_%s to %s', row[0], float(row[1]))
            cache.set('us_ratio_%s' % row[0], float(row[1]), 24*3600)


def search_interests(word):
    db = db_connect()
    query =  """select * from (select condition_id as id, name from conditions union select id, name from treatments) as s where name like '%{0}%' limit 10;""".format(word)
    logger.debug('The search query is %s', query)
    result = db.engine.execute(text(query))
    return [{'id':row[0], 'name': row[1]} for row in result]


    