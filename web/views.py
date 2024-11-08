from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from adminapp.models import NewsCategory, NewsSubCategory
from users.models import MyCategory, MySubCategory
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user:
                    if user.is_staff:
                        login(request, user)
                        return redirect("adminapp:index")
                    else:
                        login(request, user)
                        return redirect("users:index")
                else:
                    messages.success(request, "Wrong Password")
            else:
                form.add_error(None, "Invalid username, email, or password.")
        else:
            print("form is not valid")
    else:
        form = LoginForm()
    return render(request, 'web/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('web:category_select')
    else:
        form = RegistrationForm()
    return render(request, 'web/register.html', {'form': form})

def category_select(request):
    news_category = NewsCategory.objects.filter().all()
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        print(selected_categories)
        for category_id in selected_categories:
            category = NewsCategory.objects.get(id=category_id)
            MyCategory.objects.create(user=request.user, category=category)
        
        return redirect('web:sub_category_select')
    context = {
        'news_categories' : news_category
    }
    return render(request,'web/category.html',context)

def sub_category_select(request):
    user = request.user
    my_categories = MyCategory.objects.filter(user=user)
    print(my_categories)
    news_categories = [my_category.category for my_category in my_categories]
    print(news_categories)
    news_sub_categories = NewsSubCategory.objects.filter(category__in=news_categories)
    print(news_sub_categories)
    if request.method == 'POST':
        selected_sub_categories = request.POST.getlist('sub_categories')
        for sub_category_id in selected_sub_categories:
            sub_category = NewsSubCategory.objects.get(id=sub_category_id)
            category = sub_category.category
            MySubCategory.objects.create(user=request.user, category=category, sub_category=sub_category)
        return redirect('users:index')
    context = {
        'news_sub_categories' : news_sub_categories
    }
    return render(request,'web/sub_category.html',context)

def logout_view(request):
    logout(request)
    return redirect("web:login")
