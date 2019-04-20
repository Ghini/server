from django.contrib import admin

# Register your models here.
from .models import Taxon

#######################################################
class TaxonAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank', 'epithet', 'authorship', 'year', 'parent', 'accepted', )
    list_editable = ('epithet', 'authorship', 'year', )

admin.site.register(Taxon, TaxonAdmin)
