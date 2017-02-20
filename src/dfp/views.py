import json
import csv
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from dfp.models import Country, Report, Dimension, Metric, DimesionCategory

from inspire.logger import logger
from dfp.apis.report import ReportManager
# Create your views here.


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
    print request.body
    if request.method == 'GET':
        reports = [obj.as_json() for obj in Report.objects.all()]
        return JsonResponse({'result': reports})
    if request.method == 'POST':
        body = json.loads(request.body)
        report = Report(name=body['name'], query=factory_report(body), status='complete')
        report.save()
        return JsonResponse({'result': 'success'})


def generate_report(json_obj):
    dims = json_obj.get('dims')
    metrics = json_obj.get('metrics')
    country = json_obj.get


def factory_report(body):
    return json.dumps({
        'dims': [dim['id'] for dim in body['dimensions']],
        'metrics': [metric['id'] for metric in body['metrics']]
    })
    


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
            content = csv.reader(f)
            data = format_data(content, report)
        os.remove(file_name)
        return JsonResponse({'report': data})

