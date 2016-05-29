from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import JourneyList, AddJourney, DetailJourney, DeleteJourney

urlpatterns = [
    url('^$', login_required(JourneyList.as_view()), name='list-courses'),
    url('^add/$', login_required(AddJourney.as_view()), name='add-course'),
    url('^(?P<pk>\d+)/$', login_required(DetailJourney.as_view()), name='detail-course'),
    url('^(?P<pk>\d+)/delete/$', login_required(DeleteJourney.as_view()), name='delete-course'),
]
