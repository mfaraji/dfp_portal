import os
import json
import csv
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from dfp.models import Country, Report, Dimension, Metric, DimesionCategory, AdUnit, Community, Topic, ReportType

from inspire.logger import logger
from dfp.apis.report import ReportManager
from dfp.utils import ReportFormatter, SaleReportFormatter


def list_countries(request):
    objs = [obj.as_json() for obj in Country.objects.all()]
    return  JsonResponse({'result': objs})

def dimensions(request):
    # dims = {category.name: category.as_json() for category in DimesionCategory.objects.all()}
    result = []
    for category in DimesionCategory.objects.all():
        result.extend(category.as_json())
    return  JsonResponse({'result': result})


def communities(request):
    objs = [obj.as_json() for obj in Community.objects.all()]
    return  JsonResponse({'result': objs})

def topics(request):
    objs = [obj.as_json() for obj in Topic.objects.all()]
    return  JsonResponse({'result': objs})

def metrics(request):
    objs = [obj.as_json() for obj in Metric.objects.all()]
    return  JsonResponse({'result': objs})

@csrf_exempt
def reports(request):
    if request.method == 'GET':
        reports = [obj.as_json() for obj in Report.objects.all()]
        return JsonResponse({'result': reports})
    if request.method == 'POST':
        body = json.loads(request.body)
        r_type = ReportType.objects.get(name=body['type'])
        report = Report(name=body['name'], query=request.body, status='complete', user=request.user, r_type=r_type)
        report.save()
        return JsonResponse({'result': 'success'})
    

def get_ad_units(request):
    return JsonResponse({'result': [unit.as_json() for unit in AdUnit.objects.all()]})


@csrf_exempt
def report(request, pk):
    if request.method == 'DELETE':
        report = Report.objects.get(id=pk)
        if report:
            report.delete()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'failure', 'message':'Report Not Found'})
    if request.method == 'HEAD':
        report = Report.objects.get(id=pk)
        if report:
            return JsonResponse({'result':'success', 'data': report.as_json(full=True)})
    if request.method == 'GET':
        report = Report.objects.get(id=pk)
        report_params = json.loads(report.query)
        # report_manager = ReportManager()
        # job_id, file_name = report_manager.run(report)
        content = None
        logger.debug('Reading content of the report')
        FOMATTER = SaleReportFormatter if report.r_type.name == 'sale' else ReportFormatter
        with open('/tmp/tmp7rlWee.csv', 'r') as f:
            content = csv.DictReader(f)
            data = FOMATTER(content, report).format()
        # os.remove(file_name)
        return JsonResponse({'report': data})

