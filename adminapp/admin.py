from django.contrib import admin
from .models import NewsCategory, NewsSubCategory, NewsArticle

# Register your models here.

admin.site.register(NewsCategory)
admin.site.register(NewsSubCategory)
admin.site.register(NewsArticle)
