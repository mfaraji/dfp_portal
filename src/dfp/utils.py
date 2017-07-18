import re
import locale
import json

from inspire.logger import logger
from dfp.models import Community, Topic, Metric
from dfp.aws_db import update_us_users_ratio
from django.core.cache import cache

from babel.numbers import format_currency

FUTURE_METRICS = ('SELL_THROUGH_AVAILABLE_IMPRESSIONS')

locale.setlocale( locale.LC_ALL, '' )

class ReportFormatter(object):

    def __init__(self, csv_reader, report, output_format='dict'):
        self.reader = csv_reader
        self._content = {}
        self._headers = []
        self.report = report
        self.params = json.loads(report.query)
        self.is_future_report = (True if filter(lambda x: x.code in FUTURE_METRICS, self.report.metrics) else False)

    def format_headers(self):
        dims = [item.name for item in self.report.dimensions]
        metrics = []
        for metric in self.report.metrics:
            metrics.append(metric.name)
            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS':
                metrics.append('Price')
                metrics.append('Total')
        return dims + metrics

    def format(self):
        result = {
            'name': self.report.name,
            'headers': self.format_headers(),
            'dateRange': "%s - %s" % (self.params['from'], self.params['to']),
            'rows': self.format_data()
        }
        return result

    def format_data(self):
        result = []
        for row in self.reader:
            item = self._format_row(row)
            if item:
                result.append(item)
        return result

    def _format_row(self, row):
        new_row = []
        for item in self.report.dimensions:
            if item.code == 'AD_UNIT_NAME':
                if row['Ad unit 1'] != 'community' or ('Ad unit 3' in row and row['Ad unit 3'] != 'N/A'):
                    return
                ad_unit = Community.objects.filter(ad_unit_code=row['Ad unit ID 2']).first()

                if not ad_unit:
                    return
                new_row.append(ad_unit.name)
            else:
                new_row.append(row[item.column_name])

        for metric in self.report.metrics:
            value = row[metric.column_name]
            try:
                int_value = int(row[metric.column_name])
            except ValueError:
                pass
            if metric.code in ('SELL_THROUGH_AVAILABLE_IMPRESSIONS','SELL_THROUGH_FORECASTED_IMPRESSIONS'):
                int_value = int(int_value * 0.9)

            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS':
                new_row.extend(["{:,d}".format(int_value), locale.currency(ad_unit.banner_rate), locale.currency((int_value * ad_unit.banner_rate)/1000)])
            else:
                new_row.append("{:,d}".format(int_value))
        return new_row


class SaleReportFormatter(object):

    def __init__(self, csv_reader, report, summary=None, market_research=None, offers=None):
        self.reader = csv_reader
        self._content = {}
        self._headers = []
        self.report = report
        self.params = json.loads(report.query)
        self.summary = summary
        self.market_research = market_research
        self.offers = offers
        self.communities = [item['code'] for item in self.params.get('communities', [])]
        self.community_metrics = {}
        self.metrics = self.format_metrics()

    def format_metrics(self):
        metrics = []
        for metric in self.report.metrics:
            metrics.append({'name': metric.name, 'code': metric.code})
            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS':
                metrics.append({'name':'Banner Price', 'code':'banner_price'})
                metrics.append({'name':'Banner Total','code':'banner_total'})

        for metric in self.params['email_metrics']:
            metrics.append(metric)
            if metric['code'] == 'n_sent':
                metrics.append({'name':'Email Price', 'code':'email_price'})
                metrics.append({'name':'Total Emails','code':'total_emails'})
        return metrics

    def format_headers(self):
        return ['Community']+ [metric['name'] for metric in self.metrics]

    def format(self):
        return {
            'name': self.report.name,
            'dateRange': "%s - %s" % (self.params['from'], self.params['to']),
            'headers': self.format_headers(),
            'rows': self.format_rows()
        }

    def format_rows(self):
        self.community_metrics = {}
        for row in self.reader:
            formatted_row = self._format_row(row)
            if formatted_row:
                logger.debug('Adding %s to list', formatted_row[0])
                self.community_metrics[formatted_row[0]]= formatted_row[1]
        
        if self.summary:
            summary = [item for item in self.summary]
        for metric in self.params['email_metrics']:
            if metric['code'] == 'n_sent':
                for row in summary:
                    self.add_row(metric['code'], row, position=1)
            elif metric['code'] == 'n_opened':
                for row in summary:
                    self.add_row(metric['code'], row, position=2)
            elif metric['code'] == 'n_clicked':
                for row in summary:
                    self.add_row(metric['code'], row, position=3)

            elif metric['code'] == 'n_clicks':
                for row in summary:
                    self.add_row(metric['code'], row, position=4)

            elif metric['code'] == 'market_research':
                for row in self.market_research:
                    self.add_row(metric['code'], row)
            elif metric['code'] == 'offers':
                for row in self.offers:
                    self.add_row(metric['code'], row)

        result = []
        for community, values in self.community_metrics.iteritems():
            comObj = Community.objects.filter(code=community).first()
            if not comObj:
                logger.error('Community Does not exist: %s', community)
                continue
            row = [comObj.name]
            for metric in self.metrics:
                if metric['code'] in values:
                    row.append(values[metric['code']])
                else:
                    row.append(0)
            result.append(row)
        return result

    def add_row(self, metric, row, position=1):
        if not row[0]:
            return
        community = str(row[0])
        if self.communities and community not in self.communities:
            return

        if not cache.get('us_ratio_%s' % community):
            update_us_users_ratio()
        ratio = cache.get('us_ratio_%s' % community) or 1
        logger.debug('ratio for community %s is %s', community, ratio)
        if str(community) not in self.community_metrics:
            self.community_metrics[community] =  {metric: int(row[position]) * ratio}
        else:
            self.community_metrics[community][metric] = int(row[position]) * ratio

        if metric == 'n_sent':
            c = Community.objects.filter(code=community).first()
            if not c:
                logger.debug('Community Not Found: %s', community)
                return
            self.community_metrics[community]['email_price'] = locale.currency(c.email_rate)
            self.community_metrics[community]['total_emails'] = format_currency((c.email_rate * self.community_metrics[community][metric])/1000, 'USD', locale='en_US')
        logger.debug('Original %s number is: %s', metric, row[position])
        logger.debug('Filtered %s number is: %s', metric, row[position])
        self.community_metrics[community][metric] = "{:,d}".format(int(self.community_metrics[community][metric]))

    def _format_row(self, row):
        new_row = {}
        if row['Ad unit 1'] != 'community' or ('Ad unit 3' in row and row['Ad unit 3'] != 'N/A'):
            return
        community = Community.objects.filter(ad_unit_code=row['Ad unit ID 2']).first()

        if not community or (self.communities and community.code not in self.communities):
            return

        for metric in self.report.metrics:
            value = row[metric.column_name]
            try:
                int_value = int(row[metric.column_name])
            except ValueError:
                pass
            if metric.code in ('SELL_THROUGH_AVAILABLE_IMPRESSIONS','SELL_THROUGH_FORECASTED_IMPRESSIONS'):
                int_value = int(int_value * 0.9)

            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS':
                new_row.update({'SELL_THROUGH_AVAILABLE_IMPRESSIONS': "{:,d}".format(int_value), 'banner_price': locale.currency(community.banner_rate), 'banner_total': format_currency((int_value * community.banner_rate)/1000, 'USD', locale='en_US')})
            else:
                new_row[metric.code] = "{:,d}".format(int_value)
        return (community.code, new_row)

