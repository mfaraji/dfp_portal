from googleads import dfp

from .base import Resource

class CustomTargetService(Resource):
    

    def get(self):
        # Initialize appropriate service.
        custom_targeting_service = self.client.GetService('CustomTargetingService', version='v201611')

        # Create statement to get all targeting keys.
        targeting_key_statement = dfp.FilterStatement()

        all_keys = []

        # Get custom targeting keys by statement.
        while True:
            response = custom_targeting_service.getCustomTargetingKeysByStatement(targeting_key_statement.ToStatement())
            if 'results' in response:
                all_keys.extend(response['results'])
                targeting_key_statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
            print all_keys
            return all_keys
            # if all_keys:
            #     # Create a statement to select custom targeting values.
            #     query = ('WHERE customTargetingKeyId IN (%s)' %
            #         ', '.join([str(key['id']) for key in all_keys]))
            #     statement = dfp.FilterStatement(query)

            #     # Retreive a small amount of custom targeting values at a time, paging
            #     # through until all custom targeting values have been retrieved.
            #     while True:
            #         response = custom_targeting_service.getCustomTargetingValuesByStatement(statement.ToStatement())
            #         if 'results' in response:
            #             for custom_targeting_value in response['results']:
            #                 # Print out some information for each custom targeting value.
            #                 print('Custom targeting value with ID "%d", name "%s", display name '
            #                     '"%s", and custom targeting key ID "%d" was found.\n' %
            #                     (custom_targeting_value['id'], custom_targeting_value['name'],
            #                     custom_targeting_value['displayName'],
            #                     custom_targeting_value['customTargetingKeyId']))
            #                 statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            #             else:
            #                 break

            #     print '\nNumber of results found: %s' % response['totalResultSetSize']
