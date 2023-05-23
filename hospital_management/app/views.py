from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import pno


# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    return redirect("/login")

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        
        user = auth.authenticate(username = username, password = password)
        print(user)
        if user is not None:
             auth.login(request, user)
             messages.info(request, f"Welcome, {user.username}")
             if pno.objects.filter(user=user,isDoctor = False).values():
                return redirect("/userpage")
             else:
                return redirect("/doctor")
            
        elif User.objects.filter(username = username).exists():
            messages.info(request, "Password does not match")
            return redirect("/login")
        else:
            messages.info(request, "Invalid Username")
            return redirect("/login")

    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repass = request.POST['repass']
        email = request.POST['email']
        number = request.POST['pno']
        if User.objects.filter(username = username).exists():
            messages.info(request, "Username exists")
            return redirect("/signup")
        elif User.objects.filter(email = email).exists():
            messages.info(request, "Email exists")
            return redirect("/signup")
        elif pno.objects.filter(number = number).exists() and number<10000000000 and number>-1:
            messages.info(request, "Phone number already registered")
            return redirect("/signup")
        elif password != repass:
            messages.info(request, "Passwords do not match")
            return redirect("/signup")

        user = User(username = username, password = password, email = email)
        user.set_password(password)
        user.save()
        number = pno(user = user, number = number,isDoctor = False)
        number.save()
        messages.info(request, "Signup successful")
        return redirect("/login")
    else:
        return render(request, "signup.html")
    
def logout(request):
    auth.logout(request)
    return redirect("/login")

def userpage(request):
    return render(request,"hospital/userpage.html")

def user_table(request):
    return render(request,"hospital/user_table.html")

def user_stats(request):
    return render(request,"hospital/user_stats.html")

def user_new(request):
    return render(request,"hospital/user_new.html")

def user_info(request):
    return render(request,"hospital/user_info.html")



def doctor(request):
    return render(request,"doctor/doctorpage.html")
