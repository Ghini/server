from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PlantDetail, PlantList

urlpatterns = [
    path("accessions/<str:accession_code>/plants", PlantList.as_view(), name="plants"),
    path("accessions/<str:accession_code>/plants/<str:code>", PlantDetail.as_view(), name="plants"),
    #path("locations", Locations.as_view(), name="locations"),
    #path("locations/<int:pk>/plants", Plants.as_view(), name="plants"),
]
