from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'users/index.html')

def profile(request):
    return render(request,'users/profile.html')

def account(request):
    return render(request,'users/account.html')