from django.contrib import admin

# Register your models here.
from .models import Location, Plant

admin.site.register(Location)
admin.site.register(Plant)
