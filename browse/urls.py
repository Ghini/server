from django.urls import path
from .views import index, filter_json

urlpatterns = [
    path('', index, name='index'),
    path('filter/', filter_json, name='filter'),
]
