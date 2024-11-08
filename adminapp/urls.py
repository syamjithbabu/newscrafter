from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('index/',views.index,name="index"),
    path('news/',views.news,name="news"),
    path('add-news/',views.add_news,name="add_news"),
    path('detailed-news/<slug:slug>',views.detailed_news,name="detailed_news")
]