from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Journey

# Register your models here.


class JourneyAdmin(admin.ModelAdmin):
    list_display = ('customer_full_name', 'to', 'destination', 'car', 'departure_dt')
    fieldsets = (
        (None, {
            'fields': ('customer', )
        }),
        (_('Departure / Arrival'), {
            'fields': ('country', ('departure_city', 'departure_address'),
                       ('arrival_city', 'arrival_address'), 'departure_dt'),
        }),
        (_("Choose your car"), {
            'fields': ('car',)
        }),
    )

admin.site.register(Journey, JourneyAdmin)
