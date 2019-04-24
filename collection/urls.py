from django.urls import path
from .views import AccessionDetail, ContactDetail, AccessionList, ContactList

urlpatterns = [
    path("accessions/", AccessionList.as_view(), name="accessions"),
    path("accessions/<str:code>", AccessionDetail.as_view(), name="accessions"),
    path("contacts/", ContactList.as_view(), name="contacts"),
    path("contacts/<int:pk>", ContactDetail.as_view(), name="contacts"),
]
