from __future__ import unicode_literals

import datetime

from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.db.models import signals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cities_light.models import Country, City
from model_utils import FieldTracker

from ..companies.models import Cars
from ..utils.common import CommonFields

# Create your models here.


@python_2_unicode_compatible
class LocationPoint(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_('City')
    )
    address = models.CharField(
        _('Address'),
        max_length=150,
    )

    def __str__(self):
        return "{} ({})".format(
            self.address,
            self.city
        )

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('List of locations')


@python_2_unicode_compatible
class Journey(CommonFields):
    customer = models.ForeignKey(
        User,
        limit_choices_to={
            'groups__name': settings.GROUP_CUSTOMER_LABEL,
            'is_active': True,
        },
        on_delete=models.CASCADE,
        verbose_name=_('Customer'),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_("Country")
    )
    departure = models.ForeignKey(
        LocationPoint,
        verbose_name=_('Departure'),
        related_name='departure_point',
        help_text=_('Departure must be related to country selected')
    )
    departure_dt = models.DateTimeField(
        _('Start time'),
        default=datetime.datetime.now,
    )
    arrival = models.ForeignKey(
        LocationPoint,
        verbose_name=_('Arrival'),
        related_name='arrival_point',
        help_text=_('Arrival must be related to country selected')
    )
    arrival_dt = models.DateTimeField(
        _('End time'),
    )
    car = models.ForeignKey(
        Cars,
        limit_choices_to={'is_active': True},
        verbose_name=_('Car'),
    )

    car_tracker = FieldTracker()

    def __str__(self):
        return "Journey {}: {}".format(
            self.id,
            self.customer.get_full_name(),
        )

    class Meta:
        verbose_name = _("journey")
        verbose_name_plural = _("List of journey")

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return

    @classmethod
    def reserved_flag(cls, sender, instance, created, **kwargs):
        if created is True:
            instance.car.is_reserved = True
        else:
            if instance.car_tracker.has_changed('car') is True:
                previous_car = instance.car_tracker.previous('car')
                previous_car.is_reserved = False
                previous_car.save()
            instance.car.is_reserved = instance.is_active
        instance.car.save()

    @classmethod
    def post_delete_handler(cls, sender, instance, **kwargs):
        car = instance.car
        car.is_reserved = False
        car.save()

    def clean(self):
        if self.departure.city.country != self.country:
            raise ValidationError(
                {
                    'departure': _('Departure location not in country {}'.format(self.country))
                }
            )

        if self.arrival.city.country != self.country:
            raise ValidationError(
                {
                    'departure': _('Arrival location not in country {}'.format(self.country))
                }
            )

        if self.departure_dt >= self.arrival_dt:
            raise ValidationError(
                _('Date and time configuration are incoherent')
            )

        if self.car.location != self.departure.city:
            raise ValidationError(
                {'car': _('Car not available for departure from {}'.format(self.departure.city))}
            )

        if self.car_tracker.has_changed('car') is True:
            if self.car.is_reserved is True:
                raise ValidationError(
                    {'car': _('Car selected is already reserved')}
                )

signals.post_save.connect(Journey.reserved_flag, sender=Journey)
signals.post_delete.connect(Journey.post_delete_handler, sender=Journey)
