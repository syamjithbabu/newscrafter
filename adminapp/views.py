from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import NewsCategory, NewsSubCategory, NewsArticle
import pytz
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request,'adminapp/index.html')

def news(request):
    news = NewsArticle.objects.filter().order_by('-id')
    return render(request,'adminapp/news.html',{'all_news':news})

def detailed_news(request,slug):
    news = NewsArticle.objects.get(slug=slug)
    return render(request,'adminapp/detailed-news.html',{'news':news})

def add_news(request):
    news_links = fetch_news_links()
    all_news = []
    
    for link in news_links:
        article_data = fetch_full_article(link)
        all_news.append(article_data)
    
    return render(request,'adminapp/add-news.html', {'all_news':all_news})

def fetch_news_links():
    # URL of the main news briefs page
    url = "https://timesofindia.indiatimes.com/briefs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html5lib')

    # Find links to individual articles
    news_links = []
    sections = soup.find_all('div', class_='brief_box')
    
    for section in sections:
        link_tag = section.find('a')
        if link_tag and link_tag.get('href'):
            # Construct the full URL and add to list
            full_url = "https://timesofindia.indiatimes.com" + link_tag['href']
            news_links.append(full_url)
    
    return news_links


def fetch_full_article(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, 'html5lib')
    
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title"

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
    
    # Simulate category and subcategory extraction (you might need custom logic here)
    category_name = determine_category(title)  # Placeholder function for category
    sub_category_name = determine_sub_category(title)  # Placeholder function for sub-category

    # Fetch or create the category
    category, created = NewsCategory.objects.get_or_create(category_name=category_name)

    # Fetch or create the sub-category linked to the category
    sub_category, created = NewsSubCategory.objects.get_or_create(
        category=category,
        sub_category_name=sub_category_name
    )

    # Save the article
    article, created = NewsArticle.objects.get_or_create(
        title=title,
        author=author,
        date_published=date_published,
        content=full_content,
        image_url=image_url,
        category=category,
        sub_category=sub_category
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

