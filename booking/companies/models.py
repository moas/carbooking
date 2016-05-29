from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from cities_light.models import Country, City

from ..utils.common import CommonFields

# Create your models here.


class CarsReserved(models.Manager):

    def get_queryset(self):
        return super(CarsReserved, self).get_queryset().filter(is_reserved=True)


@python_2_unicode_compatible
class Companies(CommonFields):
    name = models.CharField(max_length=50)
    slug_name = models.SlugField(max_length=50, db_index=True)

    country = models.ForeignKey(Country)
    cities = models.ManyToManyField(City, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('A company')
        verbose_name_plural = _('List of companies')


@python_2_unicode_compatible
class Cars(CommonFields):
    company = models.ForeignKey(Companies, limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    location = models.ForeignKey(City)
    is_active = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)

    objects = models.Manager()
    reserved = CarsReserved()

    def __str__(self):
        return "{} ({})".format(self.description, self.company)

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Company cars')

    def clean(self):
        if self.is_active is False and self.is_reserved is True:
            raise ValidationError(
                _('Impossible to reserve car which state is disable')
            )

        if self.location.country != self.company.country:
            raise ValidationError(
                {'location': _('{} is not a valid location for {}'.format(
                    self.location,
                    self.company.country,
                ))}
            )

        if self.company.cities.exists():
            if self.location.id in self.company.cities.values_list('id', flat=True) is False:
                raise ValidationError(
                    {'location': _('Company not cover {}'.format(self.location))}
                )


