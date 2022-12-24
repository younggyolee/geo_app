from django.contrib.gis.db import models

from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

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

class PointView(GenericAPIView, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    serializer_class = PointSerializer
    queryset = models.Point.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
