import json
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from dfp.models import Country, Report, Dimension, Metric, DimesionCategory

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
        report = Report(name=body['name'], query=make_report(body), status='complete')
        report.save()
        return JsonResponse({'result': 'success'})




def make_report(params):
    report_job = {
            'reportQuery': {
                'dimensions': ['COUNTRY_NAME'],
                # 'statement': filter_statement,
                'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS'],
                # 'dateRangeType': 'CUSTOM_DATE',
                'dateRangeType': 'LAST_WEEK',
                # 'startDate': {'year': start_date.year,
                #             'month': start_date.month,
                #             'day': start_date.day},
                # 'endDate': {'year': end_date.year,
                #           'month': end_date.month,
                #           'day': end_date.day}
          }
        }
    return json.dumps(report_job)


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
        report_job = json.loads(report.query)
