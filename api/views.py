from django.contrib.gis.db import models
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from . import models

class PointSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Point
        geo_field = 'point'
        fields = [
            'id',
            'point',
        ]

class PointView(RetrieveUpdateDestroyAPIView):
    queryset = models.Point.objects.all()
    serializer_class = PointSerializer

class PointListView(ListCreateAPIView):
    queryset = models.Point.objects.all()
    serializer_class = PointSerializer
