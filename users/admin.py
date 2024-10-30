from django.contrib import admin
from .models import MyCategory, MySubCategory

# Register your models here.

admin.site.register(MyCategory)
admin.site.register(MySubCategory)
