from django.contrib import admin

# Register your models here.
from .models import Accession, Contact, Verification

class AccessionAdmin(admin.ModelAdmin):
    ordering = ['code']
    search_fields = ['code']
    autocomplete_fields = ['source']

class ContactAdmin(admin.ModelAdmin):
    ordering = ['fullname']
    search_fields = ['fullname']

class VerificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['accession', 'taxon', 'contact']

admin.site.register(Accession, AccessionAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Verification, VerificationAdmin)
