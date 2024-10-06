from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('index',views.index,name="index"),
    path('profile',views.profile,name="profile"),
    path('account',views.account,name="account")
]
