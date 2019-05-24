from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (PlantList, PlantDetail, PlantInfobox, PlantMarkup, PlantDepending, PlantCarousel,
                    LocationList, LocationDetail, LocationInfobox, LocationMarkup, LocationDepending, )
from .forms import PlantForm, LocationForm


urlpatterns = [
    # plant
    path("accession/<str:accession_code>/plant/", PlantList.as_view(), name="plant-list"),
    path("accession/<str:accession_code>/plant/form/", PlantForm.as_view(), name="plant-post-form"),
    path("accession/<str:accession_code>/plant/<str:code>/", PlantDetail.as_view(), name="plant-detail"),
    path("accession/<str:accession_code>/plant/<str:code>/form/", PlantForm.as_view(), name="plant-form"),
    path("accession/<str:accession_code>/plant/<str:code>/infobox/", PlantInfobox.as_view(), name="plant-infobox"),
    path("accession/<str:accession_code>/plant/<str:code>/markup/", PlantMarkup.as_view(), name="plant-markup"),
    path("accession/<str:accession_code>/plant/<str:code>/depending/", PlantDepending.as_view(), name="plant-depending"),
    path("accession/<str:accession_code>/plant/<str:code>/carousel/", PlantCarousel.as_view(), name="plant-carousel"),
    # location
    path("location/", LocationList.as_view(), name="location-list"),
    path("location/form/", LocationForm.as_view(), name="location-post-form"),
    path("location/<str:code>/", LocationDetail.as_view(), name="location-detail"),
    path("location/<str:code>/form/", LocationForm.as_view(), name="location-form"),
    path("location/<str:code>/infobox/", LocationInfobox.as_view(), name="location-infobox"),
    path("location/<str:code>/markup/", LocationMarkup.as_view(), name="location-markup"),
    path("location/<str:code>/depending/", LocationDepending.as_view(), name="location-depending"),
]
