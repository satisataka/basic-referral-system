import os
import hashlib
import datetime
import datetime
import uuid
import string
import secrets

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.conf import settings
from sendsms.message import SmsMessage



#manager for our custom model
class AccountManager(BaseUserManager):
	"""
		This is a manager for Account class
	"""
	use_in_migrations = True

	def _create_user(self, phone_number, username=None, password=None, email=None, **extra_fields):

		if not username:
			username = phone_number

		if not phone_number:
			raise ValueError("The given phone must be set")

		email = self.normalize_email(email)
		username = self.model.normalize_username(username)

		if phone_number:
			user = self.model(
				phone_number=phone_number,
				username=username,
				email=email,
				**extra_fields
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, phone_number, username=None, password=None, email=None,   **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(phone_number, username, password, email, **extra_fields)

	def create_superuser(self, phone_number,  password, username=None, email=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_active', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff')is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(phone_number=phone_number, username=username, password=password, email=email, **extra_fields)


class Account(AbstractUser):
	"""
	  Custom user class inheriting AbstractUser class
	"""
	username_validator = ASCIIUsernameValidator()

	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. This value may contain only English letters, numbers, and @/./+/-/_ characters.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)
	phone_number = PhoneNumberField(_('phone number'), unique=True, blank=False)
	invite = models.ForeignKey('InviteKey', on_delete=models.SET_NULL, null=True, blank=True)

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email']

	objects = AccountManager()

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('user')
		unique_together = ('phone_number', 'email', 'username')

	def __str__(self):
		return str(self.phone_number)

	def clean(self):
		try:
			self.user_invite
		except:
			InviteKey.create_invitekey_for_number(self)

		if self.invite == self.user_invite:
			raise ValidationError({'invite':_("You can't enter your invite code.")})





class PhoneToken(models.Model):
	phone_number = PhoneNumberField(editable=False)
	otp = models.CharField(max_length=40, editable=False)
	used = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)

	class Meta:
		verbose_name = _("Phone Token")
		verbose_name_plural = _("Phone Tokens")

	def __str__(self):
		return "{} - {}".format(self.phone_number, self.otp)

	@classmethod
	def create_otp_for_number(cls, number):
		'''PhoneToken generated and sent to SMS'''
		otp = cls.generate_otp(length=getattr(settings, 'ACCOUNT_PHONETOKEN_LENGTH', 4))
		phone_token = PhoneToken(phone_number=number, otp=otp)
		phone_token.save()

		from_phone = getattr(settings, 'SENDSMS_FROM_NUMBER', None)
		message = SmsMessage(
			body="Ваш код активации: {} debug:{}".format(otp, phone_token.id),
			from_phone=from_phone,
			to=[str(number)]
		)
		message.send()
		return phone_token

	@classmethod
	def generate_otp(cls, length=4):
		m = hashlib.sha256()
		m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
		m.update(os.urandom(16))
		otp = str(int(m.hexdigest(), 16))[-length:]
		return otp

class InviteKey(models.Model):
	master = models.OneToOneField(Account, unique=True, primary_key=True, related_name='user_invite', on_delete=models.CASCADE)
	key = models.CharField(max_length=40, unique=True, blank=False, null=False)

	@classmethod
	def create_invitekey_for_number(cls, user):
		'''Invitekey generated'''
		alphabet = string.ascii_letters + string.digits
		key = ''.join(secrets.choice(alphabet) for i in range(6))
		invite_key = InviteKey(master=user, key=key)
		invite_key.save()
		return invite_key

	class Meta:
		verbose_name = "Invite Key"
		verbose_name_plural = "Invite Key"

	def __str__(self):
		return "{} - {}".format(self.master, self.key)

