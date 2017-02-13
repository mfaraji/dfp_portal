from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from dfp.models import Country, Report

# Create your views here.


def list_countries(request):
	objs = [obj.as_json() for obj in Country.objects.all()]
	return  JsonResponse({'result': objs})

def list_reports(request):
	reports = [obj.as_json() for obj in Report.objects.all()]
	return JsonResponse({'result': reports})


@csrf_exempt
def report(request, pk):
	if request.method == 'DELETE':
		return JsonResponse({'result': 'success'})