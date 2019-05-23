from django.contrib import admin


# Register your models here.
from .models import Location, Plant, PlantImage

class LocationAdmin(admin.ModelAdmin):
    ordering = ['code']
    search_fields = ['name', 'code']

class PlantAdmin(admin.ModelAdmin):
    search_fields = ['code']
    autocomplete_fields = ['accession', 'location']

    def get_search_results(self, request, queryset, search_term):
        print('searching plants', search_term)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(accession__code__contains=search_term)
        try:
            acc_part, plt_part = search_term.rsplit('.', 1)
            queryset |= self.model.objects.filter(accession__code__contains=acc_part, code__contains=plt_part)
        except ValueError:
            pass
        return queryset, use_distinct


class PlantImageAdmin(admin.ModelAdmin):
    ordering = ['plant__accession__code', 'plant__code']
    autocomplete_fields = ['plant']

    def get_search_results(self, request, queryset, search_term):
        print('searching plant images', search_term)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

admin.site.register(Location, LocationAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantImage, PlantImageAdmin)
