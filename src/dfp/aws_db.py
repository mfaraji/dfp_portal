import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, and_

from django.conf import settings

def db_connect():
	return create_engine(settings.AWS_DATABASE_URL)


def activity_summary(communities=[]):
	db = db_connect()
	Session = sessionmaker(bind=db)
	meta = MetaData()
	activity_summary = Table('asat_summary', meta, autoload=True, autoload_with=db)
	session = Session()
	today = datetime.datetime.today().date()
	last_month = today - datetime.timedelta(weeks=12)
	if not communities:
		query = (select([activity_summary.c.group_id.label('community_id'), func.sum(activity_summary.c.n_sent).label('n_sent'), func.sum(activity_summary.c.n_opened).label('n_opened'), \
			func.sum(activity_summary.c.n_clicked).label('n_clicked'), func.sum(activity_summary.c.n_clicks).label('n_clicks')])\
			.where(activity_summary.c.d_sent > last_month).group_by(activity_summary.c.group_id))
	else:
		query = (select([activity_summary.c.group_id.label('community_id'), func.sum(activity_summary.c.n_sent).label('n_sent'), func.sum(activity_summary.c.n_opened).label('n_opened'), \
			func.sum(activity_summary.c.n_clicked).label('n_clicked'), func.sum(activity_summary.c.n_clicks).label('n_clicks')])\
			.where(and_(activity_summary.c.d_sent > last_month, activity_summary.c.group_id.in_(communities))).group_by(activity_summary.c.group_id))
	result = session.execute(query)
	return result
