import json
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models

from . import models

@csrf_exempt
def point(request):
    if request.method == 'GET':
        data = serializers.serialize('geojson', list(models.Point.objects.all()))
        return HttpResponse(data, content_type='application/json')
    elif request.method == 'POST':
        data = json.loads(request.body)
        x, y = data['geometry']['coordinates']
        models.Point.objects.create(point=Point(x, y))
        return HttpResponse({'ok': True})
