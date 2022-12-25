from rest_framework import serializers
from django.contrib.gis.geos import Point, Polygon
from .models import Point, Contour

def validate_coord(x, y):
    if not -180 <= x <= 180 or not -90 <= y <= 90:
        raise serializers.ValidationError('Coordinate out of range. (x, y) should be in this range: (-180 <= x <= 180) AND (-90 <= y <= 90)')

def validate_polygon(polygon: Polygon):
    if not polygon.simple:
        raise serializers.ValidationError('Only simple polygons are accepted.')

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'data']

    def validate_data(self, value: Point):
        validate_coord(value.x, value.y)
        return value

class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = ['id', 'data']

    def validate_data(self, value: Polygon):
        for x, y in value.coords[0]: validate_coord(x, y)
        validate_polygon(value)
        return value

class GEOSGeometrySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField()
