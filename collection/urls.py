from django.urls import path
from .views import (AccessionDetail, AccessionList, AccessionInfobox,
                    VerificationDetail, VerificationList,
                    ContactDetail, ContactList, ContactInfobox, )

urlpatterns = [
    path("accessions/", AccessionList.as_view(), name="accessions"),
    path("accessions/<str:code>/", AccessionDetail.as_view(), name="accession"),
    path("accessions/<str:code>/infobox/", AccessionInfobox.as_view(), name="accession-infobox"),
    path("accessions/<str:accession_code>/verifications/", VerificationList.as_view(), name="verifications"),
    path("accessions/<str:accession_code>/verifications/<int:code>/", VerificationDetail.as_view(), name="verification"),
    path("contacts/", ContactList.as_view(), name="contacts"),
    path("contacts/<int:pk>/", ContactDetail.as_view(), name="contact"),
    path("contacts/<int:pk>/infobox/", ContactInfobox.as_view(), name="contact-infobox"),
]
