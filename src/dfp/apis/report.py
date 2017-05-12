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

    if params['type'] == 'sale':
        report_job['reportQuery']['dimensions'].append('AD_UNIT_NAME')
        report_job['reportQuery']['adUnitView'] = 'HIERARCHICAL'
    else:
        for dim in params['dimensions']:
            dimobj = Dimension.objects.get(pk=dim['id'])
            if dimobj.code == 'AD_UNIT_NAME':
                report_job['reportQuery']['adUnitView'] = 'HIERARCHICAL'
            report_job['reportQuery']['dimensions'].append(str(dimobj.code))


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

    if 'communities' in params and params['communities']:
        conditions.append('PARENT_AD_UNIT_ID  IN (%s)' % ",".join([community['ad_unit_code'] for community in params['communities']]))
        # val = {
        #     'key': 'units',
        #     'value': {
        #         'xsi_type': 'NumberValue',
        #         # 'value': '64313693'
        #         'value': ",".join([community['ad_unit_code'] for community in params['communities']])
        #     }
        # }
        # values.append(val)
 

    if conditions:
        CONDITIONS = ' AND '.join(conditions)
        filter_statement = {'query': 'WHERE %s' % CONDITIONS, 'values': values}

    # if params['type'] == 'sale':
    #     report_job['reportQuery']['dateRangeType'] = 'LAST_WEEK'
    # else:
    report_job['reportQuery']['dateRangeType'] = 'CUSTOM_DATE'
    report_job['reportQuery']['startDate'] = parse_date(params['from'])
    report_job['reportQuery']['endDate'] = parse_date(params['to'])
    

    if filter_statement:
        report_job['reportQuery']['statement'] = filter_statement

    return report_job


class ReportManager(Resource):

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
