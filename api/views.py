from django.contrib.gis.db import models
from django.shortcuts import get_object_or_404
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
    def get_queryset(self):
        contour = self.request.query_params.get('contour')
        if contour is None:
            return models.Point.objects.all()
        else:
            poly = get_object_or_404(models.Contour, pk=contour)
            return models.Point.objects.filter(point__within=poly.polygon)

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
