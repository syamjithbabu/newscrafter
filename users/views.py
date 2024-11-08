from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
import requests
from django.utils import timezone
from bs4 import BeautifulSoup
import re
from adminapp.models import NewsCategory, NewsSubCategory, NewsArticle
from .models import MyCategory, MySubCategory

# Create your views here.

def index(request):
    user = request.user

    user_sub_category_ids = MySubCategory.objects.filter(user=user.id).values_list('sub_category', flat=True)

    user_sub_categories = NewsSubCategory.objects.filter(id__in=user_sub_category_ids)
    
    # Filter NewsArticles based on the user's subcategories
    news_articles = NewsArticle.objects.filter(sub_category__in=user_sub_categories).order_by('-id')

    print(news_articles)

    context = {
        'news_articles': news_articles,
    }

    return render(request,'users/index.html',context)

def profile(request):
    return render(request,'users/profile.html')

def account(request):
    return render(request,'users/account.html')
