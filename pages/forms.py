from django.test import TestCase

# Create your tests here.
from django import forms
from django.forms import ModelForm
from.models import UserEnquiryModel

class UserEnquiryForm(ModelForm):
      class Meta:
            model =UserEnquiryModel
            fields='__all__'