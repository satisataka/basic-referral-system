from tabnanny import verbose
from tkinter import Widget
from django import forms
from .models import Account, PhoneToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
	"""
	Login form
	"""
	phone_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget, help_text = _('Add a valid phone number'), label=_('Phone number'))

class ValidateForm(forms.Form):
	"""
	Validate Form
	"""
	otp = forms.CharField(widget=forms.NumberInput(), help_text = _('Enter code from SMS'), label=_('Code'))

class AddInviteCodeForm(forms.Form):
	"""
	Add Invite Code Form
	"""
	invite = forms.CharField(label=_('Invite Code'))


