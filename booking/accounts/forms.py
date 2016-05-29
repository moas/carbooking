from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.conf import settings


class CustomerCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for field in ('first_name', 'last_name', 'email'):
            self.fields[field].required = True

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2',
                  'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(CustomerCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()
        user.groups.add(Group.objects.get(name=settings.GROUP_CUSTOMER_LABEL))
