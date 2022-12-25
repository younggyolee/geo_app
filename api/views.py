import json
from django.contrib.gis.db import models
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers

from . import models

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Point
        fields = ['id', 'data']

class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contour
        fields = ['id', 'data']

class PointListView(ListCreateAPIView):
    def get_queryset(self):
        contour = self.request.query_params.get('contour')
        if contour is None:
            return models.Point.objects.all()
        else:
            poly = get_object_or_404(models.Contour, pk=contour)
            return models.Point.objects.filter(data__within=poly.data)

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

class ContourIntersectionView(GenericAPIView, RetrieveModelMixin):
    queryset = models.Contour.objects.all()
    def get(self, request: Request, *args, **kwargs):
        contour1 = self.get_object()
        contour2 = get_object_or_404(models.Contour, pk=self.request.query_params.get('contour'))
        geom = contour1.data.intersection(contour2.data)
        return Response(data=json.loads(geom.json))
