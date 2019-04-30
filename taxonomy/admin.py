from django.contrib import admin

# Register your models here.
from .models import Taxon, Rank

#######################################################
class TaxonAdmin(admin.ModelAdmin):
    ordering = ['rank', 'epithet']
    list_display = ('id', 'rank', 'epithet', 'authorship', 'year', 'parent', 'accepted', )
    list_editable = ('epithet', 'authorship', 'year', )
    autocomplete_fields = ['rank', 'parent', 'accepted']
    search_fields = ['epithet']

#######################################################
class RankAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'short', 'show_as', )
    list_editable = ('name', 'short', 'show_as', )
    search_fields = ['name']

admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Rank, RankAdmin)
