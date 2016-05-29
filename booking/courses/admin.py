from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Journey
from .forms import AdminJourneyForm

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

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = AdminJourneyForm
        return super(JourneyAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Journey, JourneyAdmin)
