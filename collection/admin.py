from django.contrib import admin

# Register your models here.
from .models import Accession, Contact

admin.site.register(Accession)
admin.site.register(Contact)
