import re

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

	def __init__(self, csv_reader, report):
		self.reader = csv_reader
		self._content = {}
		self._headers = []
		self.report = report

	def format_headers(self):
		return ['Community'] + [item.name for item in self.report.metrics]

	def format(self):
		return {
			'name': self.report.name,
			'headers': self.format_headers(),
			'rows': self.format_rows()
		}

	def format_rows(self):
		result = []
		for row in self.reader:
			formatted_row = self._format_row(row)
			if formatted_row:
				result.append(formatted_row)
		
		return sorted(result)

	def _format_row(self, row):
		# import pdb; pdb.set_trace()
		new_row = []
		# import pdb; pdb.set_trace()
		community_key_value = row['Dimension.CUSTOM_CRITERIA']
		elements = community_key_value.split('=',1)

		community = None
		if elements[0] in ('MemberComm', 'Community'):
			community = Community.objects.get(code=elements[1].rstrip('*'))
		elif elements[0] == 'Topic':
			topic = Topic.objects.get(code=elements[1].rstrip('*'))
			if topic:
				community = topic.community
		else:
			return

		if not community:
			return

		new_row.append(community.name)
		
		for item in self.report.metrics:
			value = row[item.column_name]
			try:
				value = "{:,d}".format(int(row[item.column_name]))
			except ValueError:
				pass
			new_row.append(value)
		return new_row

