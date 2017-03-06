import os
import json
import csv
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from dfp.models import Country, Report, Dimension, Metric, DimesionCategory, AdUnit

from inspire.logger import logger
from dfp.apis.report import ReportManager
from dfp.utils import ReportFormatter


def list_countries(request):
    objs = [obj.as_json() for obj in Country.objects.all()]
    return  JsonResponse({'result': objs})

def dimensions(request):
    # dims = {category.name: category.as_json() for category in DimesionCategory.objects.all()}
    result = []
    for category in DimesionCategory.objects.all():
        result.extend(category.as_json())
    return  JsonResponse({'result': result})

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
        report = Report(name=body['name'], query=request.body, status='complete', user=request.user)
        report.save()
        return JsonResponse({'result': 'success'})
    

def get_ad_units(request):
    return JsonResponse({'result': [unit.as_json() for unit in AdUnit.objects.all()]})

def format_data(content, report):
    result = {
        'name': report.name,
        'rows': [],
        'headers': []
    }
    all_headers = content.next()
    indices = []

    for dim in report.dimensions:
        indices.append(all_headers.index(dim.column_name))
        result['headers'].append(dim.name)

    for metric in report.metrics:
        indices.append(all_headers.index(metric.column_name))
        result['headers'].append(metric.name)

    for row in content:
        new_row = []
        for index in indices:
            new_row.append(row[index])
        result['rows'].append(new_row)

    return result



@csrf_exempt
def report(request, pk):
    if request.method == 'DELETE':
        report = Report.objects.get(id=pk)
        if report:
            report.delete()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'failure', 'message':'Report Not Found'})
    if request.method == 'GET':
        report = Report.objects.get(id=pk)
        report_params = json.loads(report.query)
        report_manager = ReportManager()
        job_id, file_name = report_manager.run(report)
        content = None
        logger.debug('Reading content of the report')
        with open(file_name, 'r') as f:
            content = csv.DictReader(f)
            data = ReportFormatter(content, report).format()
        # os.remove(file_name)
        return JsonResponse({'report': data})

