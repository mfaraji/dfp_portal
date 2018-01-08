# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

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


class Order(Resource):

    def get(self):
        # Initialize appropriate service.
        order_service = self.client.GetService(
            'OrderService', version='v201608')

        # Create a statement to select orders.
        statement = dfp.FilterStatement()

        # Retrieve a small amount of orders at a time, paging
        # through until all orders have been retrieved.
        while True:
            response = order_service.getOrdersByStatement(
                statement.ToStatement())
            if 'results' in response:
                for order in response['results']:
                    # Print out some information for each order.
                    print('Order with ID "%d" and name "%s" was found.\n' % (order['id'],
                                                                             order['name']))
                statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break

        print '\nNumber of results found: %s' % response['totalResultSetSize']


Order().get()
