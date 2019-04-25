from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import RankViewSet, TaxonViewSet, index

router = DefaultRouter()
router.register('ranks', RankViewSet, base_name='ranks')
router.register('taxa', TaxonViewSet, base_name='taxa')

urlpatterns = [
    #path("taxa/<int:pk>/subtaxa/", SubTaxa.as_view(), name="subtaxa"),
]

urlpatterns += router.urls
