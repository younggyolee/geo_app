from django.contrib.gis.db import models

class Point(models.Model):
    point = models.PointField()

class Contour(models.Model):
    polygon = models.PolygonField()
