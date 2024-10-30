from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    print(request.user)
    return render(request,'users/index.html')

def profile(request):
    return render(request,'users/profile.html')

def account(request): 
    user = request.user
    print(user.email)
    context = {
        'user_email' : user
    }
    return render(request,'users/account.html',context)