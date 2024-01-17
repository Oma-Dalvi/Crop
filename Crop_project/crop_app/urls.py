from django.urls import path
from .views import UserRegisterApi,UserSignInApi,HistoricalDataApi

urlpatterns = [
    path('register/', UserRegisterApi.as_view(), name='register_user'),
    path('login', UserSignInApi.as_view(), name='login_user'),
    path('historical-data', HistoricalDataApi.as_view(), name='historical_data'),
]
