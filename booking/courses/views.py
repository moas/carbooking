from django.shortcuts import redirect

from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.core.urlresolvers import reverse

from .models import Journey
from .forms import CreateJourneyForm

# Create your views here.


class JourneyList(ListView):

    model = Journey
    template_name = 'courses/list.html'

    def get_queryset(self):
        queryset = super(JourneyList, self).get_queryset()
        return queryset.filter(customer=self.request.user)


class AddJourney(CreateView):
    form_class = CreateJourneyForm
    template_name = "courses/add.html"

    def get_success_url(self):
        return reverse('courses:list-courses')

    def form_valid(self, form):
        obj = form.save()
        obj.customer = self.request.user
        obj.save()
        return redirect(self.get_success_url())


class DetailJourney(DetailView):
    model = Journey
    template_name = "courses/detail.html"

    def get_queryset(self):
        queryset = super(DetailJourney, self).get_queryset()
        return queryset.filter(customer=self.request.user)


class DeleteJourney(DeleteView):
    model = Journey
    template_name = "courses/delete.html"

    def get_queryset(self):
        queryset = super(DeleteJourney, self).get_queryset()
        return queryset.filter(customer=self.request.user)

    def get_success_url(self):
        return reverse('courses:list-courses')
