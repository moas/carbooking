from django.contrib import admin

from .models import Companies, Cars

# Register your models here.


class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_active')
    filter_horizontal = ('cities', )
    prepopulated_fields = {"slug_name": ("name",)}


class CarsAdmin(admin.ModelAdmin):
    list_display = ('company', 'location', 'description', 'is_active', 'is_reserved')

admin.site.register(Companies, CompaniesAdmin)
admin.site.register(Cars, CarsAdmin)
