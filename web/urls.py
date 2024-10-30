from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('',views.login_view,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.login_view,name="logout"),
    path('category-select/',views.category_select,name="category_select"),
    path('sub-category-select/',views.sub_category_select,name="sub_category_select")
]