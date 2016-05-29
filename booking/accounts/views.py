from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .forms import CustomerCreationForm


class CustomerCreateView(CreateView):
    form_class = CustomerCreationForm
    model = User
    template_name = "accounts/register_customer.html"

    def get_success_url(self):
        return reverse("accounts:account-login")

