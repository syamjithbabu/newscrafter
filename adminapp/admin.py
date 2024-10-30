from django.contrib import admin
from .models import NewsCategory, NewsSubCategory

# Register your models here.

admin.site.register(NewsCategory)
admin.site.register(NewsSubCategory)
