import re

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
			new_row.append("{:,d}".format(int(row[item.column_name])))
		return new_row


