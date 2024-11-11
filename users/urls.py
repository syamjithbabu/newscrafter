from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('index',views.index,name="index"),
    path('profile',views.profile,name="profile"),
    path('account',views.account,name="account"),
    path('view-news/<slug:slug>',views.view_news,name="view_news"),
    path('new-article/',views.new_article,name="new_article"),
    path('get-sub-categories/',views.sub_categories,name="sub_categories"),
    path('search/',views.search,name="search")
]
