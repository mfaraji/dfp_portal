import pprint
from googleads import dfp

from .base import Resource


def format_hierarchy(root, parents):
    result = ''
    for parent in parents:
        if parent['name'] != root:
            result += '%s > ' % parent['name']
    return result

class AdUnitService(Resource):
    

    def get(self):
        # Initialize appropriate service.
        ad_unit_service = self.client.GetService('InventoryService', version='v201611')

        # Create a statement to select ad units.
        statement = dfp.FilterStatement()
        result = []
        root_name = ''
        while True:
            response = ad_unit_service.getAdUnitsByStatement(statement.ToStatement())
            if 'results' in response:
              for ad_unit in response['results']:
                # import pdb; pdb.set_trace()
                if ad_unit['name'] == 'ca-pub-3989517083387651:':
                    continue
                if 'parentPath' not in ad_unit:
                    root_name = ad_unit['name']
                    continue

                node = {
                    'unit_id': ad_unit['id'],
                    'code': ad_unit['adUnitCode'],
                    'name': ad_unit['name'],
                    'hierarchy': format_hierarchy(root_name, ad_unit['parentPath']) + ad_unit['name'] + ' (%s)' % ad_unit['id']
                }

                print format_hierarchy(root_name, ad_unit['parentPath']) + ad_unit['name'] + '(%s)' % ad_unit['id']

                result.append(node)
              statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
              break
            # print result
            return result