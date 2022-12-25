from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Point, Contour
from .serializers import PointSerializer, ContourSerializer, GEOSGeometrySerializer

class PointListView(ListCreateAPIView):
    def get_queryset(self):
        contour_id = self.request.query_params.get('contour')
        if contour_id is None:
            return Point.objects.all()
        else:
            try:
                polygon = Contour.objects.get(pk=contour_id)
            except Contour.DoesNotExist:
                raise NotFound(f'Contour (id: {contour_id}) does not exist')
            return Point.objects.filter(data__within=polygon.data)

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
        try:
            contour1 = self.get_object()
        except Http404:
            raise NotFound(f'The first contour (id: {kwargs["pk"]}) does not exist')
        try:
            contour2_id = self.request.query_params.get('contour')
            contour2 = Contour.objects.get(pk=contour2_id)
        except Contour.DoesNotExist:
            raise NotFound(f'The second contour (id: {contour2_id}) does not exist')
        geom = contour1.data.intersection(contour2.data)
        serializer = self.get_serializer({
            'type': geom.geom_type,
            'coordinates': geom.coords
        })
        return Response(data=serializer.data)
