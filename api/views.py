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

class ContourSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Contour
        geo_field = 'polygon'
        fields = [
            'id',
            'polygon',
        ]

class PointListView(ListCreateAPIView):
    queryset = models.Point.objects.all()
    serializer_class = PointSerializer

class PointView(RetrieveUpdateDestroyAPIView):
    queryset = models.Point.objects.all()
    serializer_class = PointSerializer

class ContourListView(ListCreateAPIView):
    queryset = models.Contour.objects.all()
    serializer_class = ContourSerializer

class ContourView(RetrieveUpdateDestroyAPIView):
    queryset = models.Contour.objects.all()
    serializer_class = ContourSerializer
