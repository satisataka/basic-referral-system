import time

from django.http import Http404
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from account.models import PhoneToken, Account, InviteKey
from .serializers import PhoneTokenCreateSerializer, PhoneTokenValidateSerializer, AccountSerializer


class LoginValidateCreateAPIView(APIView):
	def post(self, request, format=None):
		if request.data.get('phone_number') and request.data.get('otp'):
			return Response({'reason': "send a request 'phone_number' or 'otp'"}, status=status.HTTP_400_BAD_REQUEST)

		if request.data.get('phone_number'): # create OTP and send SMS
			serializer = PhoneTokenCreateSerializer(data=request.data)
			if serializer.is_valid():
				token = PhoneToken.create_otp_for_number(request.data.get('phone_number'))
				phone_token = PhoneTokenCreateSerializer(token)
				data = phone_token.data
				if getattr(settings, 'SENDSMS_DUBAG', False):
					time.sleep(2)
					data['debug_otp'] = token.otp
				return Response(data)
			else:
				return Response({'reason': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

		elif request.data.get('otp'): # validate OTP and display TokenAuth
			serializer = PhoneTokenValidateSerializer(data=request.data)
			if serializer.is_valid():
				otp = request.data.get("otp")
				user = authenticate(request, otp=otp)
				if user is not None:
					login(request, user, backend='account.backend.AccountBackend')
					token, created = Token.objects.get_or_create(user=user)
					data = {
						'url_account': reverse_lazy('api:account'),
						'token': token.key
					}
					return Response(data)
				else:
					return Response({'reason': "OTP doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'reason': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'reason': "send a request 'phone_number' or 'otp'"}, status=status.HTTP_400_BAD_REQUEST)


class AccountRetrieveUpdateAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_class = AccountSerializer

	def get_object(self, pk):
		try:
			return Account.objects.get(pk=pk)
		except Account.DoesNotExist:
			raise Http404

	def get(self, request, *args, **kwargs):
		user = self.get_object(request.user.pk)
		if user:
			serializer = self.serializer_class(user)
			data = {'url_account': reverse_lazy('api:account')}
			data.update(serializer.data)
			return Response(data)

	def put(self, request, *args, **kwargs):
		user = self.get_object(request.user.pk)
		serializer = self.serializer_class(user, data=request.data, partial=True)

		if serializer.is_valid():
			if request.data.get('invite'):
				invite = request.data.get('invite')
				if user.invite:
					return Response({'invite': "You have already entered the invite code"}, status=status.HTTP_400_BAD_REQUEST)
				if user.user_invite.key == invite:
					return Response({'invite': "You can't enter your invite code."}, status=status.HTTP_400_BAD_REQUEST)

				try:
					invite_obj = InviteKey.objects.get(key=invite)
				except ObjectDoesNotExist:
					return Response({'invite': "Invite code doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

				serializer.save(invite=invite_obj)
			else:
				serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

