from django.db import models
from django.shortcuts import render

from taxonomy.models import Taxon


# Create your views here.

def index(request):
    min_rank = (Taxon.objects
                .aggregate(min_rank=models.Min('rank')))['min_rank']
    top = Taxon.objects.filter(rank=min_rank)
    return render(request, 'index.html', {'taxa': top})
