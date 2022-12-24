from django.urls import path

from . import views

urlpatterns = [
    path('points', views.point, name='point'),
]
