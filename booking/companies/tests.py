from __future__ import unicode_literals

from django.test import TestCase

from .models import Cars
from ..utils.testmixin import CompaniesMixin

# Create your tests here.


class CarsTest(TestCase, CompaniesMixin):

    @classmethod
    def setUpClass(cls):
        super(CarsTest, cls).setUpClass()

    def setUp(self):
        self.create_company()
        self.mercedes = self.create_car(desc='Mercedes X1')
        self.peugeot = self.create_car(desc='Peugeot 3008')

    def test_list_cars_reserved(self):
        retval = Cars.objects.filter(is_reserved=False, is_active=True).values_list('id', flat=True)
        self.assertEqual(len(retval), 2)
        self.assertIn(self.mercedes.id, retval)
        self.assertIn(self.peugeot.id, retval)
