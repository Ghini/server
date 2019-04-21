from django.contrib import admin

# Register your models here.
from .models import Taxon, Rank

#######################################################
class TaxonAdmin(admin.ModelAdmin):
    list_display = ('id', 'rank', 'epithet', 'authorship', 'year', 'parent', 'accepted', )
    list_editable = ('epithet', 'authorship', 'year', )

#######################################################
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short', 'show_as', )
    list_editable = ('name', 'short', 'show_as', )

admin.site.register(Taxon, TaxonAdmin)
admin.site.register(Rank, RankAdmin)
