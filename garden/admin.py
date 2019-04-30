from django.contrib import admin

# Register your models here.
from .models import Location, Plant

class LocationAdmin(admin.ModelAdmin):
    ordering = ['code']
    search_fields = ['name', 'code']

class PlantAdmin(admin.ModelAdmin):
    autocomplete_fields = ['accession', 'location']

admin.site.register(Location, LocationAdmin)
admin.site.register(Plant, PlantAdmin)
