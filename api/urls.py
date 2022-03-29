from django.urls import path
from .views import LoginValidateCreateAPIView, AccountRetrieveUpdateAPIView

app_name = 'api'

urlpatterns = [
	path('login/', LoginValidateCreateAPIView.as_view(), name='login'),
	path('account/', AccountRetrieveUpdateAPIView.as_view(), name='account'),
]
