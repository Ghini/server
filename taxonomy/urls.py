from django.urls import path
from .views import (RankList, RankDetail,
                    TaxonList, TaxonDetail, TaxonInfobox,
                    index)
from .forms import TaxonForm

urlpatterns = [
    path("taxon/", TaxonList.as_view(), name="taxon-list"),
    path("taxon//form/", TaxonForm.as_view(), name="taxon-post-form"),
    path("taxon/<int:pk>/form/", TaxonForm.as_view(), name="taxon-put-form"),
    path("taxon/<int:pk>/", TaxonDetail.as_view(), name="taxon-detail"),
    path("taxon/<int:pk>/infobox/", TaxonInfobox.as_view(), name="taxon-infobox"),
    path("rank/", RankList.as_view(), name="rank-list"),
    path("rank/<int:pk>/", RankDetail.as_view(), name="rank"),
    #path("rank/<int:pk>/infobox/", RankInfobox.as_view(), name="rank-infobox"),
    #path("taxon/<int:pk>/subtaxon/", SubTaxa.as_view(), name="subtaxon-list"),


]
