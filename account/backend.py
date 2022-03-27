import datetime
import uuid
import string
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import PhoneToken, InviteKey

class AccountBackend(ModelBackend):
	def __init__(self, *args, **kwargs):
		self.user_model = get_user_model()

	def create_user(self, phone_token, **extra_fields):
		"""
		Create and returns the user based on the phone_token.
		"""
		password = self.user_model.objects.make_random_password()
		password = extra_fields.get('password', password)

		kwargs = {
			'username': phone_token.phone_number,
			'password': password,
			'phone_number': phone_token.phone_number,
		}

		user = self.user_model.objects.create_user(**kwargs)
		return user

	def authenticate(self, request, otp=None, **extra_fields):
		'''
		1. PhoneToken verification
		2. Create new user and InviteKey for user, if he doesn't exist. But, if he exists login.
		'''
		timestamp_difference = datetime.datetime.now() - datetime.timedelta(minutes=getattr(settings, 'ACCOUNT_INVITEKEY_LIFE', 5))

		try:
			phone_token = PhoneToken.objects.get(
				otp=otp,
				used=False,
				timestamp__gte=timestamp_difference,
			)
		except PhoneToken.DoesNotExist:
			return

		user = self.user_model.objects.filter(phone_number=phone_token.phone_number).first()

		if not user:
			user = self.create_user(phone_token=phone_token,**extra_fields)
			InviteKey.create_invitekey_for_number(user)
		phone_token.used = True
		phone_token.save()

		return user
