from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import Plants

urlpatterns = [
    path("accessions/<str:accession_code>/plants", Plants.as_view(), name="plants"),
    #path("locations", Locations.as_view(), name="locations"),
    #path("locations/<int:pk>/plants", Plants.as_view(), name="plants"),
]
