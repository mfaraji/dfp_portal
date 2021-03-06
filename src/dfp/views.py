# -*- coding: utf-8 -*-
"""
View serving the requests 
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import json
import os

from aurora.query import generate_aws_report
from aurora.query import search_interests
from dfp.apis.report import ReportManager
from dfp.models import Community
from dfp.models import Country
from dfp.models import Dimension
from dfp.models import DimesionCategory
from dfp.models import Metric
from dfp.models import Report
from dfp.models import ReportType
from dfp.models import Topic
from dfp.utils import Formatter
from dfp.utils import ReportFormatter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from inspire.logger import logger


@login_required
def list_countries(request):
    objs = [obj.as_json() for obj in Country.objects.all()]
    return JsonResponse({'result': objs})


@login_required
def dimensions(request):
    # dims = {category.name: category.as_json() for category in DimesionCategory.objects.all()}
    result = []
    for category in DimesionCategory.objects.all():
        result.extend(category.as_json())
    return JsonResponse({'result': result})


@login_required
def communities(request):
    objs = [obj.as_json() for obj in Community.objects.all()]
    return JsonResponse({'result': objs})


@login_required
def topics(request):
    objs = [obj.as_json() for obj in Topic.objects.all()]
    return JsonResponse({'result': objs})


@login_required
def metrics(request):
    objs = [obj.as_json() for obj in Metric.objects.all()]
    return JsonResponse({'result': objs})


@login_required
def download_report(request, pk):
    report = Report.objects.get(id=pk)
    data = generate_report(report)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=%s.csv' % report.name
    writer = csv.writer(response)
    writer.writerow([header['name'] for header in data['headers']])
    for row in data['rows']:
        writer.writerow(row)
    return response


@csrf_exempt
@login_required
def reports(request):
    if request.method == 'GET':
        reports = [obj.as_json() for obj in Report.objects.all()]
        return JsonResponse({'result': reports})
    if request.method == 'POST':
        body = json.loads(request.body)
        r_type = ReportType.objects.get(name=body['type'])
        report = Report(name=body['name'], query=request.body,
                        status='complete', user=request.user, r_type=r_type)
        report.save()
        return JsonResponse({'result': 'success'})


@csrf_exempt
@login_required
def report(request, pk):
    if request.method == 'DELETE':
        report = Report.objects.get(id=pk)
        if report:
            report.delete()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'failure', 'message': 'Report Not Found'})
    if request.method == 'GET':
        report = Report.objects.get(id=pk)
        data = generate_report(report, cached=True)
        return JsonResponse({'report': data})

    if request.method == 'PUT':
        report = Report.objects.get(id=pk)
        delete_report_result(report)
        body = json.loads(request.body)
        r_type = ReportType.objects.get(name=body['type'])
        report.name = body['name']
        report.query = request.body
        report.r_type = r_type
        report.save()
        return HttpResponse(status=200)


@csrf_exempt
@login_required
def search(request):
    if request.method == 'GET':
        interest_name = request.GET['interest']
        logger.debug('searching for %s', interest_name)
        return JsonResponse({'result': search_interests(interest_name)})


@csrf_exempt
@login_required
def report_config(request, pk):
    report = Report.objects.get(id=pk)
    if report:
        return JsonResponse({'result': 'success', 'data': report.as_json(full=True)})


def generate_report(report, cached=True):
    cache_key = "report_result_%s" % report.id

    if cached:
        logger.debug('Loading data from cach for report %s', report.name)
        value = cache.get(cache_key)
        if value:
            logger.debug('Returning cached data')
            return json.loads(value)
    report_config = report.as_dict()
    content = None
    if report_config.get('metrics'):
        report_manager = ReportManager()
        job_id, file_name = report_manager.run(report)
        logger.debug('Reading content of the report')
        fd = open(file_name, 'r')
        content = csv.DictReader(fd)
    if report.r_type.name != 'sale':
        data = ReportFormatter(content, report).format()
    else:
        summary, market_research, offers = generate_emails_report(
            report_config)
        data = Formatter(report, dfp_content=content, asat_summary=summary,
                         market_research=market_research, offers=offers).format()
    try:
        logger.debug('Deleting file %s', file_name)
        os.remove(file_name)
    except:
        pass
    cache.set(cache_key, json.dumps(data), 3600)
    return data


def delete_report_result(report):
    cache_key = "report_result_%s" % report.id
    cache.delete(cache_key)


def generate_emails_report(report_params):
    communities = [item['code']
                   for item in report_params.get('communities', [])]
    metrics = [item['code'] for item in report_params.get('email_metrics', [])]
    interests = [str(interest['id'])
                 for interest in report_params.get('interests', [])]
    return generate_aws_report(communities=communities, metrics=metrics, interests=interests)
