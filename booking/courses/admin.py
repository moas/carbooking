from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Journey, LocationPoint

# Register your models here.


class LocationPointAdmin(admin.ModelAdmin):
    pass


class JourneyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('customer', )
        }),
        (_('Departure / Arrival'), {
            'fields': ('country', ('departure', 'departure_dt'), ('arrival', 'arrival_dt')),
        }),
        (_("Choose your car"), {
            'fields': ('car',)
        }),
    )

admin.site.register(Journey, JourneyAdmin)
admin.site.register(LocationPoint, LocationPointAdmin)
