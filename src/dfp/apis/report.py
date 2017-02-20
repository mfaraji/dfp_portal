import os
import json
from datetime import datetime, timedelta
import tempfile
from googleads import oauth2
from googleads import dfp
from googleads import errors


from dfp.models import Dimension, Metric
from inspire.logger import logger


import subprocess

SERVICE_ACCOUNT_EMAIL = 'inspire@inspire-156501.iam.gserviceaccount.com'
APPLICATION_NAME = 'inspire_web'
NETWORK_CODE = 54511533
KEY_FILE = os.path.join(os.path.dirname(__file__), 'inspire-0900e6e69fc3.p12')

class Resource(object):

    def __init__(self):
        oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
                SERVICE_ACCOUNT_EMAIL, KEY_FILE)
        self.client = dfp.DfpClient(oauth2_client, APPLICATION_NAME, network_code=NETWORK_CODE)



def make_report_job(params):
    report_job = {
            'reportQuery': {
                'dimensions': [],
                # 'statement': filter_statement,
                'columns': [],
                # 'dateRangeType': 'CUSTOM_DATE',
                'dateRangeType': 'LAST_WEEK',
                # 'startDate': {'year': start_date.year,
                #             'month': start_date.month,
                #             'day': start_date.day},
                # 'endDate': {'year': end_date.year,
                #           'month': end_date.month,
                #           'day': end_date.day}
          }
        }

    for dim in params['dims']:
        report_job['reportQuery']['dimensions'].append(str(Dimension.objects.get(pk=dim).code))

    for metric in params['metrics']:
        report_job['reportQuery']['columns'].append(Metric.objects.get(pk=metric).code)

    return report_job


class ReportManager(Resource):

    def test_query(self):
        values = [{
          'key': 'id',
          'value': {
              'xsi_type': 'NumberValue',
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
                'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS'],
                # 'dateRangeType': 'CUSTOM_DATE',
                'dateRangeType': 'LAST_WEEK',
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
        import pdb; pdb.set_trace()
        subprocess.call(['gunzip', report_file.name])

    def query_report(self, report_job):
        # values = [{
        #   'key': 'id',
        #   'value': {
        #       'xsi_type': 'NumberValue',
        #       'value': 'US'
        #   }
        # }]
        # filter_statement = {'query': 'WHERE ORDER_ID = :id',
        #     'values': values}

        # end_date = datetime.now()
        # start_date = end_date - timedelta(days=7)
        # report_job = {
        #     'reportQuery': {
        #         'dimensions': ['ADVERTISER_NAME'],
        #         # 'statement': filter_statement,
        #         'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS'],
        #         # 'dateRangeType': 'CUSTOM_DATE',
        #         'dateRangeType': 'LAST_WEEK',
        #         # 'startDate': {'year': start_date.year,
        #         #             'month': start_date.month,
        #         #             'day': start_date.day},
        #         # 'endDate': {'year': end_date.year,
        #         #           'month': end_date.month,
        #         #           'day': end_date.day}
        #   }
        # }
        print report_job
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

