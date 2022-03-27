from django.urls import path
from .views import (
	LoginView,
	ValidateView,
	AccountView,
	AddInviteView,
	LogoutView,
	EditView,
	select_lang,
	ListInviteView,
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
