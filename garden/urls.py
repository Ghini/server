from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (PlantList, PlantDetail, PlantInfobox,
                    LocationList, LocationDetail, LocationInfobox, )

urlpatterns = [
    path("accessions/<str:accession_code>/plants/", PlantList.as_view(), name="plants"),
    path("accessions/<str:accession_code>/plants/<str:code>/", PlantDetail.as_view(), name="plant"),
    path("accessions/<str:accession_code>/plants/<str:code>/infobox/", PlantInfobox.as_view(), name="plant-infobox"),
    path("locations/", LocationList.as_view(), name="locations"),
    path("locations/<str:code>/", LocationDetail.as_view(), name="location"),
    path("locations/<str:code>/infobox/", LocationInfobox.as_view(), name="location-infobox"),
    #path("locations/<int:code>/plants/", Plants.as_view(), name="plants-at-location"),
]
