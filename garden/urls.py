from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (PlantList, PlantDetail, PlantInfobox,
                    LocationList, LocationDetail, LocationInfobox, )
from .forms import PlantForm, LocationForm


urlpatterns = [
    # plant
    path("accession/<str:accession_code>/plant/", PlantList.as_view(), name="plant-list"),
    path("accession/<str:accession_code>/plant//form/", PlantForm.as_view(), name="plant-post-form"),
    path("accession/<str:accession_code>/plant/<str:code>/form/", PlantForm.as_view(), name="plant-put-form"),
    path("accession/<str:accession_code>/plant/<str:code>/", PlantDetail.as_view(), name="plant-detail"),
    path("accession/<str:accession_code>/plant/<str:code>/infobox/", PlantInfobox.as_view(), name="plant-infobox"),
    # location
    path("location/", LocationList.as_view(), name="location-list"),
    path("location//form/", LocationForm.as_view(), name="location-post-form"),
    path("location/<str:code>/form/", LocationForm.as_view(), name="location-put-form"),
    path("location/<str:code>/", LocationDetail.as_view(), name="location-detail"),
    path("location/<str:code>/infobox/", LocationInfobox.as_view(), name="location-infobox"),
]
