from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render (request, "cuentas/index.html")

def signup(request):
    return render (request, "cuentas/signup.html")

def login(request):
    return render (request, "cuentas/login.html")

def logout(request):
    pass