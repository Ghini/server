from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path("taxa/", TaxaList.as_view(), name="taxa_list"),
    #path("taxa/<int:pk>/subtaxa/", SubTaxa.as_view(), name="subtaxa"),
]
