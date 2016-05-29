from __future__ import unicode_literals

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from booking.utils.testmixin import CoursesMixin
from booking.courses.models import Journey

# Create your tests here.


class CoursesTest(TestCase, CoursesMixin):

    @classmethod
    def setUpClass(cls):
        super(CoursesTest, cls).setUpClass()

    def test_create_course(self):
        customer = self.get_customer_account()
        country = self.get_country()
        city = self.get_city()
        car = self.create_car(desc='BMW')

        course = self.get_course()
        car.refresh_from_db()

        self.assertTrue(course.car, car)
        self.assertTrue(car.is_reserved)
        self.assertTrue(course.departure_city, city)
        self.assertTrue(course.arrival_city, city)
        self.assertTrue(course.country, country)
        self.assertTrue(course.customer, customer)

    def test_car_already_reserved(self):
        self.get_country()
        self.get_city()
        car = self.create_car(desc='BMW')
        self.get_customer_account()

        self.get_course()
        car.refresh_from_db()

        self.assertTrue(car.is_reserved)

        try:
            self.create_course()
        except ValueError:
            car.refresh_from_db()
            self.assertTrue(car.is_reserved)

    def test_delete_course(self):
        self.get_country()
        self.get_city()
        car = self.create_car(desc='BMW')
        self.get_customer_account()

        course = self.get_course()
        course_id = course.id

        car.refresh_from_db()
        self.assertTrue(car.is_reserved)

        self.delete_course(course_id)
        with self.assertRaises(ObjectDoesNotExist):
            Journey.objects.get(id=course_id)
        car.refresh_from_db()
        self.assertFalse(car.is_reserved)
