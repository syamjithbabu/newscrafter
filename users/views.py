from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request,'users/index.html')

def profile(request):
    return render(request,'users/profile.html')