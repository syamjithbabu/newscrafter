from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('index/',views.index,name="index"),
    path('news/',views.news,name="news"),
    path('add-or-remove-news/',views.add_or_remove_news,name="add_or_remove_news"),
    path('add-news/',views.add_news,name="add_news"),
    path('detailed-news/<slug:slug>',views.detailed_news,name="detailed_news"),
    path('add-category/',views.add_category,name="add_category"),
    path('category-list/',views.category_list,name="category_list"),
    path('delete-category/<int:id>',views.delete_category,name="delete_category"),
    path('edit-category/<int:id>',views.edit_category,name="edit_category"),
    path('sub-category-list/',views.sub_category_list,name="sub_category_list"),
    path('add-sub-category/',views.add_sub_category,name="add_sub_category"),
    path('delete-sub-category/<int:id>',views.delete_sub_category,name="delete_sub_category"),
    path('edit-sub-category/<int:id>',views.edit_sub_category,name="edit_sub_category"),
    path('users/',views.users,name="users"),
    path('delete-user/<int:id>',views.delete_user,name="delete_user"),
    path('add-user/',views.add_user,name="add_user"),
    path('edit-user/<int:id>',views.edit_user,name="edit_user"),
    path('user-articles/',views.user_articles,name="user_articles"),
    path('accept-article/<int:id>',views.accept_news,name="accept_article"),
    path('reject-article/<int:id>',views.reject_news,name="reject_article"),
    path('accept-toi-article/<int:id>',views.accept_toi_news,name="accept_toi_article"),
    path('reject-toi-article/<int:id>',views.reject_toi_news,name="reject_toi_article")
]