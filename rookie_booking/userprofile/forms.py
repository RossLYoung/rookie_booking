from django import forms
from django.utils.translation import ugettext as _
from django.core.validators import MinLengthValidator

from .models import User


class CustomUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].validators.append(MinLengthValidator(3,message="3 characters or more"))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name' )
