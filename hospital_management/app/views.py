from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
             auth.login(request, user)
             messages.info(request, f"Welcome, {user.username}")
             return redirect("/")
        elif User.objects.filter(username = username).exists():
            messages.info(request, "Password does not match")
            return redirect("/login")
        else:
            messages.info(request, "Invalid Username")
            return redirect("/login")

    else:
        return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")
