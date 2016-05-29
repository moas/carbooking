from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout_then_login
from django.views.generic import TemplateView

from .views import CustomerCreateView

urlpatterns = [
    url(r'^register/$', CustomerCreateView.as_view(), name="account-register"),
    url(r'^profile/$', login_required(
        TemplateView.as_view(**{'template_name': 'accounts/profile.html'})), name="account-profile"),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name="account-login"),
    url(r'^logout/$', logout_then_login, name="account-logout"),
]
