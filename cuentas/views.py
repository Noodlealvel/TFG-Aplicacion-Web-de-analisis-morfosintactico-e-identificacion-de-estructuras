from turtle import end_fill
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def home(request):
    return render (request, "cuentas/index.html")

def signup(request):

    if request.method=="POST":
        username= request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        passwd2=request.POST.get('passwd2')

        user = User.objects.create_user(username, email, passwd)
        user.first_name=firstname
        user.last_name=lastname

        user.save()

        messages.success(request, "Your account was created succesfully.")

        return redirect ('signin')

    return render (request, "cuentas/signup.html")

def signin(request):
    
    if request.method=="POST":
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')

        user = authenticate(username=username, password=passwd)

        if user is not None:
            login(request, user)
            return render (request, "cuentas/index.html", {'user': request.user})
        else:
            messages.error(request, "Invalid credentials.")
            return redirect ("signin")

    return render (request, "cuentas/login.html")

@login_required
def verifyPassword(request):
    if request.method == 'POST':
        password = request.get('password')
        if request.user.check_password(password):
            return render(request, "cuentas/modifyParameters.html")
        else:
            messages.error(request, "Incorrect password.")
            return render(request, 'cuentas/verifyPassword.html')
    else:
        return render(request, "cuentas/verifyPassword.html")


def logout(request):
    pass