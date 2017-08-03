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
        self.include_cpm = self.params.get('include_cpm', True)

    def format_headers(self):
        dims = [item.name for item in self.report.dimensions]
        metrics = []
        for metric in self.report.metrics:
            metrics.append(metric.name)
            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS':
                metrics.append('Price')
                metrics.append('Total')
        _headers = dims + metrics
        return _headers

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


class Formatter(object):
    emails_metrics = []
    dfp_metrics = []

    def __init__(self, report, dfp_content=None, asat_summary=None,
        market_research=None, offers=None):
        self.report = report
        self.dfp_content = dfp_content
        self.asat_summary = asat_summary
        self.market_research = market_research
        self.offers = offers
        self.headers = {}
        self.report_config = self.report.as_dict()
        self.include_cpm = self.report_config.get('include_cpm', True)
        self.include_cps = self.report_config.get('include_cps', True)
        self.communities = [item['code'] for item in self.report_config.get('communities', [])]

    @property
    def has_dfp_result(self):
        return (self.report_config.get('metrics') != [])

    @property
    def has_emails_result(self):
        return (self.report_config.get('email_metrics') != [])

    @property
    def dfp_date_range(self):
        return 


    def format(self):
        result = {
            'name': self.report.name,
            'dfp': self.has_dfp_result,
            'emails': self.has_emails_result
        }

        if self.has_dfp_result:
            result['dateRange']= "%s - %s" % (self.report_config['from'], self.report_config['to'])

        result['headers'] = self.format_headers()

        result['rows'] = self.format_rows()

        return result


    def format_dfp_metrics(self):
        metrics = []
        for metric in self.report.metrics:
            metrics.append({'name': metric.name, 'code': metric.code, 'group':'banner'})
            if metric.code == 'SELL_THROUGH_AVAILABLE_IMPRESSIONS' and self.include_cpm:
                metrics.append({'name':'CPM Tier', 'code':'cpm_tier', 'group':'banner'})
                metrics.append({'name':'CPM','code':'cpm', 'group':'banner'})
        return metrics


    def format_emails_metrics(self):
        metrics = []
        if self.include_cps:
            metrics.append({'name':'CPS Tier', 'code':'cps_tier', 'group':'email'})
            
        for metric in self.report_config['email_metrics']:
            metrics.append(metric)
            if self.include_cps and metric['code'] == 'n_sent':
                metrics.append({'name':'CPS ASAT','code':'cps_sent', 'group':'email'})

            if self.include_cps and metric['code'] == 'market_research':
                metrics.append({'name':'CPS Market Research','code':'cps_market_research', 'group':'market_research'})

            if self.include_cps and metric['code'] == 'offers':
                metrics.append({'name':'CPS Offer','code':'cps_offer', 'group':'offer'})

        return metrics

    def format_headers(self):
        headers = [{'name':'Community', 'code': 'community', 'group':'default'}]

        if self.has_dfp_result:
            self.dfp_metrics = self.format_dfp_metrics()

        if self.has_emails_result:
            self.emails_metrics = self.format_emails_metrics()

        h = headers + self.dfp_metrics + self.emails_metrics
        logger.debug(h)
        return h

    def format_rows(self):
        self.community_metrics = {}

        if self.has_dfp_result:
            for row in self.dfp_content:
                formatted_row = self._format_dfp_row(row)
                if formatted_row:
                    logger.debug('Adding %s to list', formatted_row[0])
                    self.community_metrics[formatted_row[0]]= formatted_row[1]
          
        if self.has_emails_result:
            if self.asat_summary:
                summary = [item for item in self.asat_summary]
            for metric in self.report_config['email_metrics']:
                if metric['code'] == 'n_sent':
                    for row in summary:
                        self._format_email_row(metric['code'], row, position=1)
                elif metric['code'] == 'n_opened':
                    for row in summary:
                        self._format_email_row(metric['code'], row, position=2)
                elif metric['code'] == 'n_clicked':
                    for row in summary:
                        self._format_email_row(metric['code'], row, position=3)

                elif metric['code'] == 'n_clicks':
                    for row in summary:
                        self._format_email_row(metric['code'], row, position=4)

                elif metric['code'] == 'market_research':
                    for row in self.market_research:
                        self._format_email_row(metric['code'], row)
                elif metric['code'] == 'offers':
                    for row in self.offers:
                        self._format_email_row(metric['code'], row)

        result = []
        for community, values in self.community_metrics.iteritems():
            comObj = Community.objects.filter(code=community).first()
            row = [comObj.name]
            for metric in self.dfp_metrics + self.emails_metrics:
                if metric['code'] in values:
                    row.append(values[metric['code']])
                else:
                    row.append('NA')
            result.append(row)
        return result


    def _format_dfp_row(self, row):
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
                new_row.update({'SELL_THROUGH_AVAILABLE_IMPRESSIONS': "{:,d}".format(int_value), 'cpm_tier': '1', 'cpm': format_currency((int_value * community.banner_rate)/1000, 'USD', locale='en_US')})
            else:
                new_row[metric.code] = "{:,d}".format(int_value)
        return (community.code, new_row)


    def _format_email_row(self, metric, row, position=1):
        if not row[0]:
            return
        community = Community.objects.filter(code=str(row[0])).first()         
        
        if not community:
            logger.error('Community Not Found: %s', community)
            return

        if self.communities and community.code not in self.communities:
            return

        if not cache.get('us_ratio_%s' % community.code):
            update_us_users_ratio()
        ratio = cache.get('us_ratio_%s' % community.code) or 1
        logger.debug('ratio for community %s is %s', community.code, ratio)
        if str(community.code) not in self.community_metrics:
            self.community_metrics[community.code] =  {metric: int(row[position]) * ratio}
        else:
            self.community_metrics[community.code][metric] = int(row[position]) * ratio

        if self.include_cps and not self.community_metrics[community.code].get('cps_tier'):
            self.community_metrics[community.code]['cps_tier'] = '1'

        if metric == 'n_sent' and self.include_cps:
            self.community_metrics[community.code]['cps_sent'] = format_currency((community.email_rate * self.community_metrics[community.code][metric])/1000, 'USD', locale='en_US')
        if metric == 'market_research' and self.include_cps:
            self.community_metrics[community.code]['cps_market_research'] = format_currency((community.email_rate * self.community_metrics[community.code][metric])/1000, 'USD', locale='en_US')

        if metric == 'offers' and self.include_cps:
            self.community_metrics[community.code]['cps_offer'] = format_currency((community.email_rate * self.community_metrics[community.code][metric])/1000, 'USD', locale='en_US')
        
        self.community_metrics[community.code][metric] = "{:,d}".format(int(self.community_metrics[community.code][metric]))
