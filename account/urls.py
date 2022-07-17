from django.urls import path 
from .views import index, create_account, login_user, logout_user

app_name = 'account'

urlpatterns = [
    path("", index, name='index'),
    path("create-account/", create_account, name='create_account'),
    path("account-login/", login_user, name="login"),
    path("account-logout/", logout_user, name="logout_user"),
]
