from django.urls import path
from .views import index, filter_json
from .forms import TaxonForm, AccessionForm, VerificationForm, ContactForm, PlantForm, LocationForm

urlpatterns = [
    path('', index, name='index'),
    path('filter/', filter_json, name='filter'),

    # taxonomy
    path("taxon/form/", TaxonForm.as_view(), name="taxon-post-form"),
    path("taxon/<int:pk>/form/", TaxonForm.as_view(), name="taxon-put-form"),

    # collection
    path("accession/form/", AccessionForm.as_view(), name="accession-post-form"),
    path("accession/<int:pk>/form/", AccessionForm.as_view(), name="accession-put-form"),
    path("accession/<str:accession_code>/verifications/form/", VerificationForm.as_view(), name="verification-post-form"),
    path("accession/<str:accession_code>/verifications/<int:seq>/form/", VerificationForm.as_view(), name="verification-put-form"),
    path("contact/form/", ContactForm.as_view(), name="contact-post-form"),
    path("contact/<int:pk>/form/", ContactForm.as_view(), name="contact-put-form"),

    # garden
    path("accession/<str:accession_code>/plants/form/", PlantForm.as_view(), name="plant-post-form"),
    path("accession/<str:accession_code>/plants/<str:code>/form/", PlantForm.as_view(), name="plant-put-form"),
    path("location/form/", LocationForm.as_view(), name="location-post-form"),
    path("location/<str:code>/form/", LocationForm.as_view(), name="location-put-form"),
    
]
