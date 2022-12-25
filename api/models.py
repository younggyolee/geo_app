from django.contrib.gis.db import models

class Point(models.Model):
    data = models.PointField()

class Contour(models.Model):
    data = models.PolygonField()
