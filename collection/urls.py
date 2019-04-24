from django.urls import path
from .views import (AccessionDetail, ContactDetail, VerificationDetail,
                    AccessionList, ContactList, VerificationList, )

urlpatterns = [
    path("accessions/", AccessionList.as_view(), name="accessions"),
    path("accessions/<str:code>", AccessionDetail.as_view(), name="accessions"),
    path("accessions/<str:accession_code>/verifications/", VerificationList.as_view(), name="verifications"),
    path("accessions/<str:accession_code>/verifications/<int:code>", VerificationDetail.as_view(), name="verifications"),
    path("contacts/", ContactList.as_view(), name="contacts"),
    path("contacts/<int:pk>", ContactDetail.as_view(), name="contacts"),
]
