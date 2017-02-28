import os
import json
from datetime import datetime, timedelta
import tempfile
from googleads import dfp
from googleads import errors


from dfp.models import Dimension, Metric
from inspire.logger import logger

from .base import Resource

import subprocess


def parse_date(date_str):
    date_obj =  datetime.strptime(date_str, '%m/%d/%Y')
    return {
        'year': date_obj.year,
        'month': date_obj.month,
        'day': date_obj.day
    }

def make_report_job(params):
    report_job = {
            'reportQuery': {
                'dimensions': [],
                # 'statement': filter_statement,
                'columns': [],
                # 'dateRangeType': 'CUSTOM_DATE',
                # 'dateRangeType': 'LAST_WEEK',
                # 'startDate': {'year': start_date.year,
                #             'month': start_date.month,
                #             'day': start_date.day},
                # 'endDate': {'year': end_date.year,
                #           'month': end_date.month,
                #           'day': end_date.day}
          }
        }

    values = []
    filter_statement = {}
    conditions = []

    for dim in params['dimensions']:
        report_job['reportQuery']['dimensions'].append(str(Dimension.objects.get(pk=dim['id']).code))

    for metric in params['metrics']:
        report_job['reportQuery']['columns'].append(Metric.objects.get(pk=metric['id']).code)

    if 'country' in params:
        conditions.append('COUNTRY_NAME = :country')
        val = {
            'key': 'country',
            'value': {
                'xsi_type': 'TextValue',
                'value': params['country']['name']
            }
        }
        values.append(val)

    if 'ad_units' in params and params['ad_units']:
        conditions.append('PARENT_AD_UNIT_ID  IN (:units)')
        val = {
            'key': 'units',
            'value': {
                'xsi_type': 'NumberValue',
                # 'value': '64313693'
                'value': ",".join([str(ad_unit['id']) for ad_unit in params['ad_units']])
            }
        }
        values.append(val)


    if conditions:
        CONDITIONS = ' AND '.join(conditions)
        filter_statement = {'query': 'WHERE %s' % CONDITIONS, 'values': values}

    # val = {
    #         'key': 'condition',
    #         'value': {
    #             'xsi_type': 'TextValue',
    #             'value': '"chaos=2"'
    #         }
    #     }
    # filter_statement = {'query': 'WHERE CUSTOM_CRITERIA = ',
    #         'values': []}

    if params['daterange']['type'] =='custom':
        report_job['reportQuery']['dateRangeType'] = 'CUSTOM_DATE'
        report_job['reportQuery']['startDate'] = parse_date(params['daterange']['start'])
        report_job['reportQuery']['endDate'] = parse_date(params['daterange']['end'])

    if filter_statement:
        report_job['reportQuery']['statement'] = filter_statement

    return report_job


class ReportManager(Resource):

    def test_query(self):
        values = [{
          'key': 'id',
          'value': {
              'xsi_type': 'TextValue',
              'value': 'US'
          }
        }]
        filter_statement = {'query': 'WHERE ORDER_ID = :id',
            'values': values}

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        report_job = {
            'reportQuery': {
                'dimensions': ['COUNTRY_NAME'],
                'statement': filter_statement,
                'columns': ['AD_SERVER_IMPRESSIONS_OUT_OF_NETWORK'],
                # 'dateRangeType': 'CUSTOM_DATE',
                # 'dateRangeType': 'LAST_WEEK',
                # 'startDate': {'year': start_date.year,
                #             'month': start_date.month,
                #             'day': start_date.day},
                # 'endDate': {'year': end_date.year,
                #           'month': end_date.month,
                #           'day': end_date.day}
          }
        }
        report_downloader = self.client.GetDataDownloader(version='v201611')
        try:
            report_job_id = report_downloader.WaitForReport(report_job)
        except errors.DfpReportError, e:
            print 'Failed to generate report. Error was: %s' % e
        export_format = 'CSV_DUMP'
        report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)
        report_downloader.DownloadReportToFile(
            report_job_id, export_format, report_file)
        report_file.close()
        print 'Report job with id \'%s\' downloaded to:\n%s' % (
                report_job_id, report_file.name)
        subprocess.call(['gunzip', report_file.name])
        print report_file.name[:-3] 


    def query_report(self, report_job):
        logger.info(report_job)
        report_downloader = self.client.GetDataDownloader(version='v201611')
        try:
            report_job_id = report_downloader.WaitForReport(report_job)
        except errors.DfpReportError, e:
            logger.error('Failed to generate report. Error was: %s' % e)
            raise Exception('Coud not run the report')
        export_format = 'CSV_DUMP'
        report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)
        report_downloader.DownloadReportToFile(
            report_job_id, export_format, report_file)
        report_file.close()
        logger.debug('Report job with id \'%s\' downloaded to:\n%s' % (
                report_job_id, report_file.name))
        subprocess.call(['gunzip', report_file.name])
        return report_job_id, report_file.name[:-3]        

    def run(self, report):
        logger.debug('Query report %s', report.name)
        report_job = make_report_job(json.loads(report.query))
        return self.query_report(report_job)
