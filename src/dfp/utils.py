import re
import json

from dfp.models import Community, Topic
class ReportFormatter(object):

	def __init__(self, csv_reader, report):
		self.reader = csv_reader
		self._content = {}
		self._headers = []
		self.report = report


	def format_headers(self):
		return [item.name for item in self.report.dimensions+ self.report.metrics]

	def format(self):
		return {
			'name': self.report.name,
			'headers': self.format_headers(),
			'rows': sorted([self._format_row(row) for row in self.reader], key=lambda item: item[0])
		}
			

	def _format_row(self, row):
		# import pdb; pdb.set_trace()
		new_row = []
		for item in self.report.dimensions:
			if item.code == 'AD_UNIT_NAME':
				hierarchy = []
				for key, value in row.iteritems():
					if re.match('Ad unit [1-9]', key) and value != 'N/A':
						hierarchy.append(key)
				new_row.append(' > '.join([row[key] for key in sorted(hierarchy)]))
			else:
				new_row.append(row[item.column_name])

		for item in self.report.metrics:
			value = row[item.column_name]
			try:
				value = "{:,d}".format(int(row[item.column_name]))
			except ValueError:
				pass
			new_row.append(value)
		return new_row


class SaleReportFormatter(object):

	def __init__(self, csv_reader, emails_stat, report):
		self.reader = csv_reader
		self._content = {}
		self._headers = []
		self.report = report
		self.params = json.loads(report.query)
		self.emails_stat = emails_stat
		self.communities = [item['code'] for item in self.params.get('communities', [])]

	def format_headers(self):
		return ['Community'] + [item.name for item in self.report.metrics] + [item['name'] for item in self.params['email_metrics']]

	def format(self):
		return {
			'name': self.report.name,
			'headers': self.format_headers(),
			'rows': self.format_rows()
		}

	def format_rows(self):
		result = {}
		
		for row in self.reader:
			formatted_row = self._format_row(row)
			if formatted_row:
				result[formatted_row[0]]= formatted_row[1]
		
		order = [item['code'] for item in self.params['email_metrics']]
		stats = [stat for stat in self.emails_stat]
		for stat in stats:
			row = dict(stat)
			if not row['community_id']:
				continue
			community = str(row['community_id'])
			if str(community) not in result:
				continue
			formatted_row = self.format_stat(row, order)
			# import pdb; pdb.set_trace()
			# if not formatted_row[0] in result:
			# 	result[formatted_row[0]] = [0] * len(self.report.metrics) + formatted_row[1]
			# else:
			result[community] = result[community] + formatted_row
		
		return sorted(result.values())

	def format_stat(self, stat, order):
		result = []
		for code in order:
			result.append(str(stat[code]))

		return result

	def _format_row(self, row):
		# import pdb; pdb.set_trace()
		new_row = []
		
		community_key_value = row['Dimension.CUSTOM_CRITERIA']
		elements = community_key_value.split('=',1)

		community = None
		if elements[0] in ('MemberComm', 'Community'):
			community = Community.objects.get(code=elements[1].rstrip('*'))
		elif elements[0] == 'Topic':
			topic = Topic.objects.get(code=elements[1].rstrip('*'))
			if topic:
				community = topic.community

		if not community or (self.communities and community.code not in self.communities):
			return

		new_row.append(community.name)
		
		for item in self.report.metrics:
			value = row[item.column_name]
			try:
				value = "{:,d}".format(int(row[item.column_name]))
			except ValueError:
				pass
			new_row.append(value)
		return (community.code, new_row)

