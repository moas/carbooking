from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone

from .models import Journey
from ..companies.models import Cars


class CreateJourneyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateJourneyForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Cars.objects.filter(
            is_active=True,
            is_reserved=False,
        )

    class Meta:
        model = Journey
        exclude = ('customer', 'is_active', )

    def order_fields(self, field_order):
        super(CreateJourneyForm, self).order_fields(field_order)
        dt_field = self.fields.pop('departure_dt')
        self.fields['departure_dt'] = dt_field

    def clean_car(self):
        car = self.cleaned_data['car']
        if car.is_reserved is True:
            raise forms.ValidationError(_('Car selected is not available'))

        departure_city = self.cleaned_data['departure_city']
        if car.location != departure_city:
            raise forms.ValidationError(_('Car selected not found in {}'.format(departure_city)))
        return car

    def clean_departure_dt(self):
        dt = self.cleaned_data['departure_dt']
        if dt < timezone.now():
            raise forms.ValidationError(_('The departure time is not correct'))
        return dt

    def _departure_arrival_city(self, field_name):
        field = self.cleaned_data[field_name]
        country = self.cleaned_data['country']
        if field.country != country:
            raise forms.ValidationError(_("{} is not valid for {}".format(field, country)))
        return field

    def clean_departure_city(self):
        return self._departure_arrival_city('departure_city')

    def clean_arrival_city(self):
        return self._departure_arrival_city('arrival_city')

    def clean_arrival_address(self):
        departure = self.cleaned_data['departure_address']
        arrival = self.cleaned_data['arrival_address']
        if departure == arrival:
            raise forms.ValidationError('Arrival address must be different to departure address')
        return arrival

    def save(self, commit=True):
        obj = super(CreateJourneyForm, self).save(commit=False)
        return obj


class AdminJourneyForm(CreateJourneyForm):

    def __init__(self, *args, **kwargs):
        super(AdminJourneyForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = Cars.objects.filter(
            is_active=True,
        )

    class Meta:
        model = Journey
        fields = '__all__'

