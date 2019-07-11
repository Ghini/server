from django.contrib import admin, gis

# Register your models here.
from .models import Accession, Contact, Verification, Institution

class AccessionAdmin(admin.ModelAdmin):
    ordering = ['code']
    search_fields = ['code']
    autocomplete_fields = ['source']

class ContactAdmin(admin.ModelAdmin):
    ordering = ['fullname']
    list_display = ('id', 'fullname', 'user', )
    list_editable = ('fullname', 'user', )
    search_fields = ['fullname']

class VerificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['accession', 'taxon', 'contact']

class InstitutionAdmin(gis.admin.OSMGeoAdmin):
    default_lon = -8406734
    default_lat = 1166305
    default_zoom = 13

admin.site.register(Accession, AccessionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(Institution, InstitutionAdmin)
