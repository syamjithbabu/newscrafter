from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register")
]