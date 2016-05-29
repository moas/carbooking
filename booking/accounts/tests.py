from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import Client
from booking.utils.testmixin import CustomerMixin


class CustomerTest(TestCase, CustomerMixin):

    @classmethod
    def setUpClass(cls):
        super(CustomerTest, cls).setUpClass()
        cls.data = {
            'username': 'eli',
            'password1': 'azerty147',
            'password2': 'azerty147',
            'first_name': 'Musk',
            'last_name': 'Elon',
            'email': 'elon.musk@mail.com'
        }

    def test_create_customer_account(self):
        self.assertEqual(User.objects.count(), 0)
        self.create_customer_account(self.data)
        user = User.objects.get(username='eli', groups__name=settings.GROUP_CUSTOMER_LABEL)
        self.assertEqual(user.email, 'elon.musk@mail.com')

    def test_login(self):
        client = Client()

        customer = self.get_customer_account()

        response = client.get(reverse('index'), follow=True)
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertTrue(settings.LOGIN_URL in response.redirect_chain[1][0])

        client.force_login(customer)
        response = client.get(reverse('index'), follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual('/', reverse('index'))

    def test_logout(self):
        client = Client()

        customer = self.get_customer_account()
        client.force_login(customer)
        response = client.get(reverse('index'), follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual('/', reverse('index'))

        client.get(reverse('accounts:account-logout'), follow=True)
        response = client.get(reverse('index'), follow=True)
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertTrue(settings.LOGIN_URL in response.redirect_chain[1][0])
