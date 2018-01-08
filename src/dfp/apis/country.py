# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import tempfile

from googleads import dfp
from googleads import oauth2

SERVICE_ACCOUNT_EMAIL = 'inspire@inspire-156501.iam.gserviceaccount.com'
APPLICATION_NAME = 'inspire_web'
NETWORK_CODE = 54511533
KEY_FILE = './inspire-0900e6e69fc3.p12'


class Resource(object):

    def __init__(self):
        oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
                                                          SERVICE_ACCOUNT_EMAIL, KEY_FILE)
        self.client = dfp.DfpClient(
            oauth2_client, APPLICATION_NAME, network_code=NETWORK_CODE)


class Country(Resource):

    def get(self):
        report_downloader = self.client.GetDataDownloader(version='v201605')
        output_file = tempfile.NamedTemporaryFile(
            prefix='geo_target_type_', suffix='.csv', mode='w', delete=False)

        values = [{
            'key': 'type',
            'value': {
                'xsi_type': 'TextValue',
                'value': 'Country'
            }
        }]

        pql_query = ('SELECT Name, CountryCode FROM Geo_Target '
                     'WHERE targetable = true AND Type = :type')

        report_downloader.DownloadPqlResultToCsv(
            pql_query, output_file, values)
        output_file.close()

        print ('Saved geo targets to... %s' % output_file.name)


Country().get()
