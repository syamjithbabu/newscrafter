from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request,'web/login.html')

def register(request):
    print("working")
    return render(request,'web/register.html')
