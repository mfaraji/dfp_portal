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


class Target(Resource):
    

    def get(self):
        # Initialize appropriate service.
          constant_data_service = self.client.GetService(
              'ConstantDataService', version='v201605')

          # Get all languages.
          languages = constant_data_service.getLanguageCriterion()

          # Display results.
          for language in languages:
            print ('Language with name \'%s\' and ID \'%s\' was found.'
                   % (language['name'], language['id']))

          # Get all carriers.
          carriers = constant_data_service.getCarrierCriterion()

          # Display results.
          for carrier in carriers:
            print ('Carrier with name \'%s\', ID \'%s\', and country code \'%s\' was '
                   'found.' % (
                       carrier['name'], carrier['id'],
                       getattr(carrier, 'countryCode', 'N/A')))

    def get_campaign_targeting_criteria(self):
        # Initialize appropriate service.
        campaign_criterion_service = self.client.GetService(
          'CampaignCriterionService', version='v201605')

        # Construct selector and get all campaign targets.
        offset = 0
        selector = {
          'fields': ['CampaignId', 'Id', 'CriteriaType', 'PlatformName',
                     'LanguageName', 'LocationName', 'KeywordText'],
          'predicates': [{
              'field': 'CriteriaType',
              'operator': 'IN',
              'values': ['KEYWORD', 'LANGUAGE', 'LOCATION', 'PLATFORM']
          }],
          'paging': {
              'startIndex': str(offset),
              'numberResults': str(PAGE_SIZE)
          }
        }
        more_pages = True
        while more_pages:
            page = campaign_criterion_service.get(selector)

            # Display results.
            if 'entries' in page:
              for campaign_criterion in page['entries']:
                negative = ''
                if (campaign_criterion['CampaignCriterion.Type']
                    == 'NegativeCampaignCriterion'):
                  negative = 'Negative '
                criterion = campaign_criterion['criterion']
                criteria = (criterion['text'] if 'text' in criterion else
                            criterion['platformName'] if 'platformName' in criterion
                            else criterion['name'] if 'name' in criterion else
                            criterion['locationName'] if 'locationName' in criterion
                            else None)
                print ('%sCampaign Criterion found for Campaign ID %s with type %s and '
                       'criteria "%s".' % (negative, campaign_criterion['campaignId'],
                                           criterion['type'], criteria))
            else:
              print 'No campaign targets were found.'
            offset += PAGE_SIZE
            selector['paging']['startIndex'] = str(offset)
            more_pages = offset < int(page['totalNumEntries'])



Target().get_campaign_targeting_criteria()