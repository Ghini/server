from django.urls import path
from .views import (AccessionDetail, AccessionList, AccessionInfobox, AccessionMarkup, AccessionDepending,
                    VerificationDetail, VerificationList,
                    ContactDetail, ContactList, ContactInfobox, ContactMarkup, ContactDepending, )
from .forms import AccessionForm, VerificationForm, ContactForm


urlpatterns = [
    # accession
    path("accession/", AccessionList.as_view(), name="accession-list"),
    path("accession/form/", AccessionForm.as_view(), name="accession-post-form"),
    path("accession/<str:code>/", AccessionDetail.as_view(), name="accession-detail"),
    path("accession/<str:code>/form/", AccessionForm.as_view(), name="accession-put-form"),
    path("accession/<str:code>/infobox/", AccessionInfobox.as_view(), name="accession-infobox"),
    path("accession/<str:code>/markup/", AccessionMarkup.as_view(), name="accession-markup"),
    path("accession/<str:code>/depending/", AccessionDepending.as_view(), name="accession-depending"),
    # verification
    path("accession/<str:accession_code>/verification/", VerificationList.as_view(), name="verification-list"),
    path("accession/<str:accession_code>/verification/form/", VerificationForm.as_view(), name="verification-post-form"),
    path("accession/<str:accession_code>/verification/<int:seq>/", VerificationDetail.as_view(), name="verification-detail"),
    path("accession/<str:accession_code>/verification/<int:seq>/form/", VerificationForm.as_view(), name="verification-put-form"),
    # contact
    path("contact/", ContactList.as_view(), name="contact-list"),
    path("contact/form/", ContactForm.as_view(), name="contact-post-form"),
    path("contact/<int:pk>/", ContactDetail.as_view(), name="contact-detail"),
    path("contact/<int:pk>/infobox/", ContactInfobox.as_view(), name="contact-infobox"),
    path("contact/<int:pk>/form/", ContactForm.as_view(), name="contact-put-form"),
    path("contact/<int:pk>/markup/", ContactMarkup.as_view(), name="contact-markup"),
    path("contact/<int:pk>/depending/", ContactDepending.as_view(), name="contact-depending"),
]
