from googleads import dfp

from .base import Resource


class AdUnit(Resource):
    

    def get(self):
        # Initialize appropriate service.
        ad_unit_service = self.client.GetService('InventoryService', version='v201611')

        # Create a statement to select ad units.
        statement = dfp.FilterStatement()

        # Retrieve a small amount of ad units at a time, paging
        # through until all ad units have been retrieved.
        while True:
        response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
        if 'results' in response:
          for ad_unit in response['results']:
            # Print out some information for each ad unit.
            print('Ad unit with ID "%s" and name "%s" was found.\n' %
                  (ad_unit['id'], ad_unit['name']))
          statement.offset += dfp.SUGGESTED_PAGE_LIMIT
        else:
          break

        print '\nNumber of results found: %s' % response['totalResultSetSize']


