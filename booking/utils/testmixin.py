from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client
from django.utils.text import slugify
from cities_light.forms import CityForm, CountryForm, Country, City

from booking.companies.models import Cars, Companies
from booking.courses.models import Journey
from booking.courses.forms import CreateJourneyForm


class CustomerMixin(object):

    def create_group(self):
        return Group.objects.create(name=settings.GROUP_CUSTOMER_LABEL)

    def get_group(self):
        if Group.objects.filter(name=settings.GROUP_CUSTOMER_LABEL).exists() is False:
            self.create_group()
        return Group.objects.filter(name=settings.GROUP_CUSTOMER_LABEL).first()

    def create_customer_account(self, data={}):
        self.get_group()
        data = data or {
            'username': 'eli',
            'password1': 'azerty147',
            'password2': 'azerty147',
            'first_name': 'Musk',
            'last_name': 'Elon',
            'email': 'elon.musk@mail.com'
        }
        assert isinstance(data, dict)
        client = Client()
        response = client.post(
            reverse('accounts:account-register'),
            data
        )
        assert response.status_code == 302

    def get_customer_account(self):
        if User.objects.filter(groups__name=settings.GROUP_CUSTOMER_LABEL).exists() is False:
            self.create_customer_account()
        return User.objects.filter(groups__name=settings.GROUP_CUSTOMER_LABEL).first()

    def create_journey(self):
        pass


class LocationMixin(object):

    def create_country(self, data={}):
        data = data or {'name': 'France', 'continent': 'EU'}
        assert isinstance(data, dict)
        form = CountryForm(data)
        return form.save()

    def get_country(self):
        if Country.objects.exists() is False:
            self.create_country()
        return Country.objects.first()

    def create_city(self, data={}):
        data = data or {'name': 'Paris', 'country': self.get_country().pk}
        assert isinstance(data, dict)
        form = CityForm(data)
        return form.save()

    def get_city(self):
        if City.objects.exists() is False:
            self.create_city()
        return City.objects.first()


class CompaniesMixin(LocationMixin):

    def create_company(self, name=None):
        assert name is None or isinstance(name, str)
        return Companies.objects.create(
            name=name or 'Padam',
            slug_name='padam' if name is None else slugify(name),
            country=self.get_country(),
        )

    def get_company(self):
        if Companies.objects.exists() is False:
            self.create_company()
        return Companies.objects.first()

    def create_car(self, desc=None):
        desc = desc or 'Mercedes X1'
        assert isinstance(desc, unicode)
        return Cars.objects.create(
            company=self.get_company(),
            description=desc,
            location=self.get_city(),
        )

    def get_car(self):
        if Cars.objects.exists() is False:
            self.create_car()
        return Cars.objects.first()


class CoursesMixin(CustomerMixin, CompaniesMixin):

    def create_course(self, data={}):
        customer = self.get_customer_account()
        country = self.get_country()
        city = self.get_city()
        car = self.get_car()

        if not data:
            data = {
                'country': country.id,
                'departure_city': city.id,
                'departure_address': '37 boulevard des Riches',
                'arrival_city': city.id,
                'arrival_address': '37 rue St Joseph',
                'car': car.id,
                'departure_dt': timezone.now() + timezone.timedelta(hours=2),
            }
        assert isinstance(data, dict)

        form = CreateJourneyForm(data)
        obj = form.save()
        obj.customer = customer
        obj.save()
        return obj

    def delete_course(self, _id):
        assert isinstance(_id, int)
        course = Journey.objects.get(id=_id)
        course.delete()

    def get_course(self):
        if Journey.objects.exists() is False:
            self.create_course()
        return Journey.objects.first()
