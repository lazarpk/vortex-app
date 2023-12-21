from django.urls import path
from .views import RegisterUser, UserInfo

app_name='users'

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register-user'),
    path('user', UserInfo.as_view(), name='user-info')
]
