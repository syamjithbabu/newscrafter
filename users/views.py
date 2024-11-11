from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
import requests
from django.utils import timezone
from bs4 import BeautifulSoup
import re
from adminapp.models import NewsCategory, NewsSubCategory, NewsArticle
from .models import MyCategory, MySubCategory
from django.http import JsonResponse
from pytz import timezone as pytz_timezone
import pytz
from django.utils.text import slugify

# Create your views here.

def index(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()

    user = request.user

    user_sub_category_ids = MySubCategory.objects.filter(user=user.id).values_list('sub_category', flat=True)

    user_sub_categories = NewsSubCategory.objects.filter(id__in=user_sub_category_ids)
    
    # Filter NewsArticles based on the user's subcategories
    news_articles = NewsArticle.objects.filter(sub_category__in=user_sub_categories,date_published=current_date,status=True).order_by('-id')[:4]

    print(news_articles)

    context = {
        'news_articles': news_articles,
    }

    return render(request,'users/index.html',context)

def profile(request):
    return render(request,'users/profile.html')

def account(request):
    return render(request,'users/account.html')

def view_news(request,slug):
    news = get_object_or_404(NewsArticle,slug=slug)
    share_url = 'http://127.0.0.1:8000/'
    context = {
        'news' : news,
        'share_url' : share_url
    }
    return render(request,'users/view-news.html',context)


def new_article(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()
    categories = NewsCategory.objects.filter().all()
    sub_categories = NewsSubCategory.objects.filter().all()
    user = request.user
    if request.method == 'POST':
        category_id = request.POST.get('category')
        sub_category_id = request.POST.get('sub-category')
        title = request.POST.get('title')
        image = request.POST.get('image')
        content = request.POST.get('content')
        category = get_object_or_404(NewsCategory,id=category_id)
        sub_category = get_object_or_404(NewsSubCategory,id=sub_category_id)
        add_article = NewsArticle.objects.create(author=user,date_published=current_date,image=image,category=category,sub_category=sub_category,title=title,content=content,status=False)

    context = {
        'categories' : categories,
        'sub_categories' : sub_categories
    }
    return render(request,'users/new-article.html',context)

def sub_categories(request):
    print("hello")
    category_id = request.GET.get('category_id')
    category_instance = NewsCategory.objects.get(id=category_id)
    print(category_instance)
    sub_categories = NewsSubCategory.objects.filter(category=category_instance).values('id', 'sub_category_name')
    print(sub_categories)
    return JsonResponse({'sub_categories': list(sub_categories)})

def search(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()
    query = request.GET.get('q')
    print(query)
    user = request.user

    user_sub_category_ids = MySubCategory.objects.filter(user=user.id).values_list('sub_category', flat=True)

    user_sub_categories = NewsSubCategory.objects.filter(id__in=user_sub_category_ids)
    if query:
        search_results = NewsArticle.objects.filter(sub_category__in=user_sub_categories,date_published=current_date,title__icontains=query, status=True) | \
                         NewsArticle.objects.filter(sub_category__in=user_sub_categories,date_published=current_date,content__icontains=query, status=True)
        print(search_results)
    else:
        search_results = NewsArticle.objects.none()

    context = {
        'news_articles': search_results,
        'query': query,
    }
    return render(request, 'users/search.html', context)