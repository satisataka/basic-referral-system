from django.urls import path
from .views import (
	LoginView, ValidateView,
	AddInviteView, ListInviteView,
	AccountView, LogoutView,
	EditView, select_lang,
)

app_name = 'account'

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('validate/', ValidateView.as_view(), name='validate'),
	path('logout/', LogoutView, name='logout'),
	path('edit/', EditView.as_view(), name='edit'),
	path('add_invite/', AddInviteView.as_view(), name='add_invite'),
	path('list_invite/', ListInviteView.as_view(), name='list_invite'),
	path('<str:code>/', select_lang, name='select_lang'),
	path('', AccountView, name='account'),
]
