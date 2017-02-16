from datetime import datetime, timedelta
import tempfile
from googleads import oauth2
from googleads import dfp
from googleads import errors


import subprocess

SERVICE_ACCOUNT_EMAIL = 'inspire@inspire-156501.iam.gserviceaccount.com'
APPLICATION_NAME = 'inspire_web'
NETWORK_CODE = 54511533
KEY_FILE = './inspire-0900e6e69fc3.p12'


class Resource(object):

    def __init__(self):
        oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
                SERVICE_ACCOUNT_EMAIL, KEY_FILE)
        self.client = dfp.DfpClient(oauth2_client, APPLICATION_NAME, network_code=NETWORK_CODE)


class ReportGenerator(object):
    _report_job = {
        'reportQuery': {
            'dimensions': [],
            'dimensionAttributes': [],
            'statement': None,
            'columns':[],
            'dateRangeType': 'CUSTOM_DATE',
            'startDate': None,
            'endDate': None
        }
    }

    def add_start_date(self, start_date):
        self._report_job['startDate'] = {
            'year': start_date.year,
            'month': start_date.month,
            'day': start_date.day
        }

    def add_end_date(self, end_date):
        self._report_job['endDate'] = {
            'year': end_date.year,
            'month': start_date.month,
            'day': start_date.day
        }

class Report(Resource):

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
        subprocess.Popen(['gunzip', report_file.name])
        return report_job_id, report_file.name[:-3]        


Report().test_query()
