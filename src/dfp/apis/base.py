from googleads import oauth2

from django.conf import settings


KEY_FILE = './inspire-0900e6e69fc3.p12'

SERVICE_ACCOUNT_EMAIL = 'inspire@inspire-156501.iam.gserviceaccount.com'
APPLICATION_NAME = 'inspire_web'
NETWORK_CODE = 54511533

class Resource(object):

	def __init__(self):
		oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
				SERVICE_ACCOUNT_EMAIL, KEY_FILE)
		self.client = dfp.DfpClient(oauth2_client, APPLICATION_NAME, network_code=NETWORK_CODE)




