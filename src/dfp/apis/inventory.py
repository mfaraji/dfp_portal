from googleads import oauth2
from googleads import dfp

SERVICE_ACCOUNT_EMAIL = 'inspire@inspire-156501.iam.gserviceaccount.com'
APPLICATION_NAME = 'inspire_web'
NETWORK_CODE = 54511533
KEY_FILE = './inspire-0900e6e69fc3.p12'


class Resource(object):

    def __init__(self):
        oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
                SERVICE_ACCOUNT_EMAIL, KEY_FILE)
        self.client = dfp.DfpClient(oauth2_client, APPLICATION_NAME, network_code=NETWORK_CODE)


class AdUnit(Resource):
    

    def get(self):
        # Initialize appropriate service.
        ad_unit_service = self.client.GetService('InventoryService', version='v201611')

        # Create a statement to select ad units.
        statement = dfp.FilterStatement()
        # import pdb; pdb.set_trace()
        # Retrieve a small amount of ad units at a time, paging
        # through until all ad units have been retrieved.
        while True:
            response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
            if 'results' in response:
              for ad_unit in response['results']:
                # Print out some information for each ad unit.
                print ad_unit
                import pdb; pdb.set_trace()
                # print('Ad unit with ID "%s" and name "%s" was found.\n' %
                #       (ad_unit['id'], ad_unit['name']))
              statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
              break

        print '\nNumber of results found: %s' % response['totalResultSetSize']

AdUnit().get()