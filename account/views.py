import time

from django.http import Http404, HttpResponseRedirect
from django.utils import translation
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, logout, login, get_user_model, get_user
from django.views.generic import FormView
from django.core.exceptions import  ValidationError
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from account.models import Account
from .forms import LoginForm, ValidateForm, AddInviteCodeForm
from .models import PhoneToken, InviteKey, Account


def AccountView(request):
	return render(request, 'account/account.html')

def LogoutView(request):
	logout(request)
	return HttpResponseRedirect(reverse_lazy('account:account'))

def select_lang(request, code):
	go_next = request.META.get('HTTP_REFERER', '/')
	response = HttpResponseRedirect(go_next)
	if code and translation.check_for_language(code):
		response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code)
		translation.activate(code)
	return response


class LoginView(FormView):
	"""sign up user view"""
	form_class = LoginForm
	template_name = 'account/login.html'

	def form_valid(self, form):
		""" process user login"""
		phone_number = form.cleaned_data['phone_number']
		token = PhoneToken.create_otp_for_number(phone_number)
		from_phone = getattr(settings, 'SENDSMS_FROM_NUMBER')
		time.sleep(2)
		if getattr(settings, 'SENDSMS_DUBAG', True):
			messages.add_message(
				self.request,
				messages.INFO,
				'Код авторизации: {}'.format(token.otp),
				extra_tags='Сообщение от: {}'.format(from_phone),
			)

		return HttpResponseRedirect(reverse_lazy('account:validate'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('account:account'))
		return super().get(request, *args, **kwargs)


class ValidateView(FormView):
	"""Validate up user view"""
	form_class = ValidateForm
	template_name = 'account/validate.html'

	def form_valid(self, form):
		otp = form.cleaned_data['otp']
		user = authenticate(self.request, otp=otp)

		if user is not None:
			login(self.request, user)
			return HttpResponseRedirect(reverse_lazy('account:account'))
		else:
			form.add_error('otp', _('Incorrect code'))
			return render(self.request, self.template_name, {'form': form})

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('account:account'))
		return super().get(request, *args, **kwargs)


class EditView(UpdateView):
	"""
	View forms for editing an account
	"""
	template_name = 'account/edit_account.html'
	model = Account
	fields = ['username', 'first_name', 'last_name', 'email']
	success_url = reverse_lazy('account:account')

	def get_object(self, queryset=None):
		if self.request.user.is_authenticated:
			self.kwargs['pk'] = self.request.user.pk
		else:
			raise Http404
		return super().get_object(queryset)


class AddInviteView(FormView):
	"""
	View the field for entering the invite code and valid it
	"""
	form_class = AddInviteCodeForm
	template_name = 'account/add_invite.html'

	def form_valid(self, form):
		invite_code = form.cleaned_data['invite']
		try:
			invite_code = InviteKey.objects.get(key=invite_code)
		except:
			form.add_error('invite', _('This code does not exist.'))
			return render(self.request, self.template_name, {'form': form})

		user = get_user(self.request)

		if user.invite:
			form.add_error('invite', _('You have already entered an invite code.'))
			return render(self.request, self.template_name, {'form': form})

		user.invite = invite_code

		try:
			user.full_clean()
		except ValidationError as e:
			invite_field_errors = e.message_dict['invite']
			form.add_error('invite', invite_field_errors)
			return render(self.request, self.template_name, {'form': form})
		user.save()
		return HttpResponseRedirect(reverse_lazy('account:account'))

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('account:account'))
		return super().get(request, *args, **kwargs)


class ListInviteView(ListView):
	"""
	View list of accounts that entered the user's invite code
	"""
	model = get_user_model()
	template_name = 'account/list_invite.html'

	def get_queryset(self):
		user = get_user(self.request)
		if user.is_authenticated:
			print(user.user_invite)
			print(self.model.objects.filter(invite=user.user_invite))
			return self.model.objects.filter(invite=user.user_invite)
		else:
			raise Http404

