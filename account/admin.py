from django.contrib import admin
from .models import Account, InviteKey, PhoneToken
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _



class AccountAdmin(UserAdmin):
	fieldsets = (
			(None, {'fields': ('username', 'password', 'invite')}),
			(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
			(_('Permissions'), {
				'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
			}),
			(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		)

admin.site.register(Account, AccountAdmin)
admin.site.register(InviteKey)
admin.site.register(PhoneToken)
