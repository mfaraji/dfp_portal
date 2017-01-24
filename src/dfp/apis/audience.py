from googleads import dfp

from .base import Resource




class AudienceSegment(Resource):

    def get(self):
        # Initialize appropriate service.
        audience_segment_service = self.client.GetService(
          'AudienceSegmentService', version='v201611')
        query = 'WHERE type = :type'
        values = [
          {'key': 'type',
           'value': {
               'xsi_type': 'TextValue',
               'value': 'FIRST_PARTY'
           }},
        ]
        # Create a statement to select audience segments.
        statement = dfp.FilterStatement(query, statement)

        # Retrieve a small amount of audience segments at a time, paging
        # through until all audience segments have been retrieved.
        while True:
            response = audience_segment_service.getAudienceSegmentsByStatement(
                statement.ToStatement())
            if 'results' in response:
              for audience_segment in response['results']:
                # Print out some information for each audience segment.
                print('Audience segment with ID "%d", name "%s", and size "%d" was '
                      'found.\n' % (audience_segment['id'], audience_segment['name'],
                                    audience_segment['size']))
              statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
              break

            print '\nNumber of results found: %s' % response['totalResultSetSize']

    def create(self, custom_targeting_key_id, custom_targeting_value_id):
        # Initialize appropriate services.
        audience_segment_service = self.client.GetService(
          'AudienceSegmentService', version='v201611')
        network_service = self.client.GetService('NetworkService', version='v201611')

        # Get the root ad unit ID used to target the entire network.
        root_ad_unit_id = (
          network_service.getCurrentNetwork()['effectiveRootAdUnitId'])

        # Create inventory targeting (pointed at root ad unit i.e. the whole network)
        inventory_targeting = {
          'targetedAdUnits': [
              {'adUnitId': root_ad_unit_id}
          ]
        }

        # Create custom criteria.
        custom_criteria = [
          {
              'xsi_type': 'CustomCriteria',
              'keyId': custom_targeting_key_id,
              'valueIds': [custom_targeting_value_id],
              'operator': 'IS'
          }
        ]

        # Create the custom criteria set.
        top_custom_criteria_set = {
          'logicalOperator': 'AND',
          'children': custom_criteria
        }

        # Create the audience segment rule.
        rule = {
          'inventoryRule': inventory_targeting,
          'customCriteriaRule': top_custom_criteria_set
        }

        # Create an audience segment.
        audience_segment = [
          {
              'xsi_type': 'RuleBasedFirstPartyAudienceSegment',
              'name': ('Sports enthusiasts audience segment %s' %
                       uuid.uuid4()),
              'description': 'Sports enthusiasts between the ages of 20 and 30',
              'pageViews': '6',
              'recencyDays': '6',
              'membershipExpirationDays': '88',
              'rule': rule
          }
        ]

        audience_segments = (
          audience_segment_service.createAudienceSegments(audience_segment))

        for created_audience_segment in audience_segments:
        print ('An audience segment with ID \'%s\', name \'%s\', and type \'%s\' '
               'was created.' % (created_audience_segment['id'],
                                 created_audience_segment['name'],
                                 created_audience_segment['type']))


    def update(self, audience_segment_id):
        # Initialize appropriate service.
        audience_segment_service = self.client.GetService(
          'AudienceSegmentService', version='v201611')

        # Create statement object to get the specified first party audience segment.
        values = (
          [{'key': 'type',
            'value': {
                'xsi_type': 'TextValue',
                'value': 'FIRST_PARTY'
                }
           },
           {'key': 'audience_segment_id',
            'value': {
                'xsi_type': 'NumberValue',
                'value': audience_segment_id
                }
           }])
        query = 'WHERE Type = :type AND Id = :audience_segment_id'
        statement = dfp.FilterStatement(query, values, 1)

        # Get audience segments by statement.
        response = audience_segment_service.getAudienceSegmentsByStatement(
          statement.ToStatement())

        if 'results' in response:
        updated_audience_segments = []
        for audience_segment in response['results']:
          print ('Audience segment with id \'%s\' and name \'%s\' will be updated.'
                 % (audience_segment['id'], audience_segment['name']))

          audience_segment['membershipExpirationDays'] = '180'
          updated_audience_segments.append(audience_segment)

        audience_segments = audience_segment_service.updateAudienceSegments(
            updated_audience_segments)

        for audience_segment in audience_segments:
          print ('Audience segment with id \'%s\' and name \'%s\' was updated' %
                 (audience_segment['id'], audience_segment['name']))
        else:
        print 'No audience segment found to update.'