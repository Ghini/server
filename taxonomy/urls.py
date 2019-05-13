from django.urls import path, re_path
from .views import (RankList, RankDetail,
                    TaxonList, TaxonDetail, TaxonInfobox, TaxonMarkup, TaxonDepending,
                    index)
from .forms import TaxonForm

urlpatterns = [
    path("taxon/", TaxonList.as_view(), name="taxon-list"),
    path("taxon/form/", TaxonForm.as_view(), name="taxon-post-form"),
    path("taxon/<int:pk>/", TaxonDetail.as_view(), name="taxon-detail"),
    path("taxon/<int:pk>/form/", TaxonForm.as_view(), name="taxon-put-form"),
    path("taxon/<int:pk>/infobox/", TaxonInfobox.as_view(), name="taxon-infobox"),
    path("taxon/<int:pk>/markup/", TaxonMarkup.as_view(), name="taxon-markup"),
    path("taxon/<int:pk>/depending/", TaxonDepending.as_view(), name="taxon-depending"),
    path("rank/", RankList.as_view(), name="rank-list"),
    path("rank/<int:pk>/", RankDetail.as_view(), name="rank-detail"),
    #path("rank/<int:pk>/infobox/", RankInfobox.as_view(), name="rank-infobox"),
    #path("taxon/<int:pk>/subtaxon/", SubTaxa.as_view(), name="subtaxon-list"),


]
