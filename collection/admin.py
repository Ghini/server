from django.contrib import admin

# Register your models here.
from .models import Accession, Contact, Verification

admin.site.register(Accession)
admin.site.register(Contact)
admin.site.register(Verification)
