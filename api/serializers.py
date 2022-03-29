from rest_framework import serializers
from phonenumber_field.formfields import PhoneNumberField
from account.models import PhoneToken, Account, InviteKey

class PhoneTokenCreateSerializer(serializers.ModelSerializer):
	phone_number = serializers.CharField(validators=PhoneNumberField().validators)
	class Meta:
		model = PhoneToken
		fields = ('phone_number',)


class PhoneTokenValidateSerializer(serializers.ModelSerializer):
	otp = serializers.CharField(max_length=40)
	class Meta:
		model = PhoneToken
		fields = ('otp',)


class ListAccountInviteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('phone_number',)
		read_only_fields = ('phone_number',)


class InviteKeySerializer(serializers.ModelSerializer):
	account_set = ListAccountInviteSerializer(many=True,)
	class Meta:
		model = InviteKey
		fields = ('pk', 'key', 'account_set')


class AccountSerializer(serializers.ModelSerializer):
	invite = serializers.SlugRelatedField(read_only=True, slug_field='key')
	user_invite = InviteKeySerializer()

	class Meta:
		model = Account
		fields = ('phone_number', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'invite', 'user_invite')
		read_only_fields = ('phone_number', 'last_login', 'date_joined', 'user_invite',)

