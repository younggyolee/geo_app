import json
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers

from .models import Point, Contour

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'data']

class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ['id', 'data']

class GEOSGeometrySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField()

class PointListView(ListCreateAPIView):
    def get_queryset(self):
        contour = self.request.query_params.get('contour')
        if contour is None:
            return Point.objects.all()
        else:
            poly = get_object_or_404(Contour, pk=contour)
            return Point.objects.filter(data__within=poly.data)

    serializer_class = PointSerializer

class PointView(RetrieveUpdateDestroyAPIView):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

class ContourListView(ListCreateAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

class ContourView(RetrieveUpdateDestroyAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

class ContourIntersectionView(RetrieveAPIView):
    queryset = Contour.objects.all()
    serializer_class = GEOSGeometrySerializer

    def retrieve(self, request: Request, *args, **kwargs):
        contour1 = self.get_object()
        contour2 = get_object_or_404(Contour, pk=self.request.query_params.get('contour'))
        geom = contour1.data.intersection(contour2.data)
        serializer = self.get_serializer(json.loads(geom.json))
        return Response(data=serializer.data)
        
