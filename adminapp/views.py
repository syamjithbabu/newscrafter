from django.shortcuts import get_object_or_404, render, redirect
import requests
from bs4 import BeautifulSoup
from .models import NewsCategory, NewsSubCategory, NewsArticle
import pytz
from django.utils import timezone
from web.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from web.forms import RegistrationForm
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.text import slugify

# Create your views here.

def index(request):
    news = NewsArticle.objects.filter(status=True).order_by('-id')
    return render(request,'adminapp/index.html',{'all_news':news})

def news(request):
    news = NewsArticle.objects.filter(status=True).order_by('-id')
    return render(request,'adminapp/news.html',{'all_news':news})

def detailed_news(request,slug):
    news = NewsArticle.objects.get(slug=slug)
    return render(request,'adminapp/detailed-news.html',{'news':news})

def detailed_news_two(request,slug):
    news = NewsArticle.objects.get(slug=slug)
    return render(request,'adminapp/detailed-news-2.html',{'news':news})

def user_articles(request):
    news = NewsArticle.objects.filter(status=False).exclude(author='Unknown author')
    print(news)
    context = {
        'all_news' : news
    }
    return render(request,'adminapp/user-articles.html',context)

def accept_news(request,id):
    article_update = NewsArticle.objects.filter(id=id).update(status=True)
    return redirect('adminapp:user_articles')

def reject_news(request,id):
    article = get_object_or_404(NewsArticle,id=id)
    article.delete()
    return redirect('adminapp:user_articles')

def accept_toi_news(request,id):
    article_update = NewsArticle.objects.filter(id=id).update(status=True)
    return redirect('adminapp:add_or_remove_news')

def reject_toi_news(request,id):
    article = get_object_or_404(NewsArticle,id=id)
    article.delete()
    return redirect('adminapp:add_or_remove_news')

def add_news(request):
    news_links = fetch_news_links()
    all_news = []
    
    for link in news_links:
        article_data = fetch_full_article(link)
        all_news.append(article_data)
    
    return redirect('adminapp:add_or_remove_news')

def add_or_remove_news(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()
    all_news = NewsArticle.objects.filter(date_published=current_date, status=False).order_by('-id')
    context = {
        'all_news' : all_news
    }
    return render(request,'adminapp/add-news.html',context)

def fetch_news_links():
    url = "https://timesofindia.indiatimes.com/briefs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')

    news_links = []
    sections = soup.find_all('div', class_='brief_box')
    title_tag = soup.find('h2')
    title_text = title_tag.get_text()  # Extract text from the HTML tag
    slug = slugify(title_text)
    
    for section in sections:
        if NewsArticle.objects.filter(slug=slug):
            print("Already fetched")
            continue
        link_tag = section.find('a')
        if link_tag and link_tag.get('href'):
            full_url = "https://timesofindia.indiatimes.com" + link_tag['href']
            news_links.append(full_url)
    
    return news_links

def fetch_full_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html5lib')
    
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title"
    
    # Check if an article with the same title already exists
    if NewsArticle.objects.filter(title=title).exists():
        print(f"Article with title '{title}' already exists. Skipping.")
        return None

    author_tag = soup.find('span', class_='auth_detail')
    author = author_tag.text.strip() if author_tag else "Unknown author"

    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()
    date_published = current_date

    content_tags = soup.find_all('div', class_='js_tbl_article')
    article_content = [paragraph.text.strip() for paragraph in content_tags]
    full_content = " ".join(article_content)

    image_tag = soup.find('img', alt=title)
    image_url = image_tag['src'] if image_tag else None

    category_name = determine_category(title)
    sub_category_name = determine_sub_category(title)

    category, created = NewsCategory.objects.get_or_create(category_name=category_name)

    sub_category, created = NewsSubCategory.objects.get_or_create(
        category=category,
        sub_category_name=sub_category_name
    )

    article, created = NewsArticle.objects.get_or_create(
        title=title,
        author=author,
        date_published=date_published,
        content=full_content,
        image_url=image_url,
        category=category,
        sub_category=sub_category,
        status=False
    )

    return {
        'title': title,
        'author': author,
        'date_published': date_published,
        'content': full_content,
        'image_url': image_url,
        'category': category.category_name,
        'sub_category': sub_category.sub_category_name
    }


def determine_category(title):
    # Placeholder function for extracting category based on title or other criteria
    if "election" in title.lower():
        return "Politics"
    elif "business" in title.lower():
        return "Business"
    # Add more logic as needed
    return "General"

def determine_sub_category(title):
    # Placeholder function for extracting sub-category based on title or other criteria
    if "stock" in title.lower():
        return "Stock Market"
    elif "technology" in title.lower():
        return "Technology News"
    # Add more logic as needed
    return "General News"

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        new_category = NewsCategory.objects.create(category_name=category_name)
        return redirect('adminapp:category_list')
    return render(request,'adminapp/add-new-category.html')

def category_list(request):
    categories = NewsCategory.objects.filter().order_by('-id')
    context = {
        'categories' : categories
    }
    return render(request,'adminapp/category-list.html',context)

def delete_category(request,id):
    category = get_object_or_404(NewsCategory,id=id)
    print(category)
    category.delete()
    return redirect('adminapp:category_list')

def edit_category(request,id):
    category = get_object_or_404(NewsCategory,id=id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        new_category = NewsCategory.objects.filter(category_name=category).update(category_name=category_name)
        return redirect('adminapp:category_list')
    return render(request,'adminapp/edit-category.html',{'category':category})

def sub_category_list(request):
    sub_categories = NewsSubCategory.objects.filter().order_by('-id')
    context = {
        'sub_categories' : sub_categories
    }
    return render(request,'adminapp/sub-category-list.html',context)

def add_sub_category(request):
    categories = NewsCategory.objects.filter()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = get_object_or_404(NewsCategory,category_name=category_name)
        sub_category_name = request.POST.get('sub_category_name')
        new_sub_category = NewsSubCategory.objects.create(category=category,sub_category_name=sub_category_name)
        return redirect('adminapp:sub_category_list')
    context = {
        'categories' : categories
    }
    return render(request,'adminapp/add-sub-category.html',context)

def delete_sub_category(request,id):
    sub_category = get_object_or_404(NewsSubCategory,id=id)
    sub_category.delete()
    return redirect('adminapp:sub_category_list')

def edit_sub_category(request,id):
    sub_category = get_object_or_404(NewsSubCategory,id=id)
    if request.method == 'POST':
        category = sub_category.category
        sub_category_name = request.POST.get('sub_category_name')
        edit_sub_category = NewsSubCategory.objects.filter(category=category,sub_category_name=sub_category.sub_category_name).update(sub_category_name=sub_category_name)
        print(edit_sub_category,"SUb Category")
        return redirect('adminapp:sub_category_list')
    return render(request,'adminapp/edit-sub-category.html',{'sub_category':sub_category})

def users(request):
    users = CustomUser.objects.filter().exclude(username='admin')
    print(users)
    context = {
        'users' : users
    }
    return render(request,'adminapp/users.html',context)

def delete_user(request,id):
    print(id)
    user = get_object_or_404(CustomUser,id=id)
    print(user)
    user.delete()
    return redirect('adminapp:users')

def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('adminapp:users')
    else:
        form = RegistrationForm()
    print(form)
    context = {
        'form' : form
    }
    return render(request,'adminapp/add-user.html',context)

def edit_user(request,id):
    user = get_object_or_404(CustomUser,id=id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:index')
    else:
        form = AdminPasswordChangeForm(user=user)
    context = {
        'form' : form
    }
    return render(request,'adminapp/edit-user.html',context)

def accept_all(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_date = timezone.now().astimezone(ist).date()
    all_news = NewsArticle.objects.filter(date_published=current_date,author='Unknown author',status=False)
    all_news.update(status=True)
    return redirect('adminapp:add_or_remove_news')

def search(request):
    query = request.GET.get('q')
    print(query)
    if query:
        search_results = NewsArticle.objects.filter(title__icontains=query, status=True) | \
                         NewsArticle.objects.filter(content__icontains=query, status=True)
        print(search_results)
    else:
        search_results = NewsArticle.objects.none()

    context = {
        'all_news': search_results,
        'query': query,
    }
    return render(request, 'adminapp/search.html', context)