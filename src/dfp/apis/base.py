from googleads import oauth2

from django.conf import settings


KEY_FILE = './inspire-0900e6e69fc3.p12'


class Resource(object):

	def __init__(self):
		oauth2_client = oauth2.GoogleServiceAccountClient(oauth2.GetAPIScope('dfp'),
				settings.SERVICE_ACCOUNT_EMAIL, KEY_FILE)
		self.client = dfp.DfpClient(oauth2_client, settings.APPLICATION_NAME, network_code=settings.NETWORK_CODE)




