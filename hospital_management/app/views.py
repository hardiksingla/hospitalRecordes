from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import CustomUser, doctorsMore


# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    return redirect("/login")

def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, f"Welcome, {user.username}")
            print(user.type)
            if user.type == "hospital":
                return redirect("/userpage")
            else:
                return redirect("/doctor")
            
        elif CustomUser.objects.filter(username = username).exists():
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
        if CustomUser.objects.filter(username = username).exists():
            messages.info(request, "Username exists")
            return redirect("/signup")
        elif CustomUser.objects.filter(email = email).exists():
            messages.info(request, "Email exists")
            return redirect("/signup")
        elif CustomUser.objects.filter(pno = number).exists():
            messages.info(request, "Phone number already registered")
            return redirect("/signup")
        elif password != repass:
            messages.info(request, "Passwords do not match")
            return redirect("/signup")

        user = CustomUser(username = username, email = email, pno = number)
        user.set_password(password)
        user.save()
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
    if request.method == "POST":

        name = request.POST["name"]
        age = request.POST["age"]
        dob = request.POST["dob"]
        pno = request.POST["phone1"]
        altpno = request.POST["phone2"]
        speciality = request.POST["speciality"]
        degree = request.POST["degree"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        gender = request.POST.get("gender")

        user = CustomUser(username = username, first_name = name, pno = pno, email = email)
        user.set_password(password)
        user.save()
        more = doctorsMore(doctor = user, altpno = altpno, speciality = speciality, degree = degree, dob = dob, gender = gender)
        more.save()
    return render(request,"hospital/user_new.html")

def user_info(request):
    return render(request,"hospital/user_info.html")



def doctor(request):
    return render(request,"doctor/doctorpage.html")
def doctor_info_edit(request):
    return render(request,"doctor/doctor_info_edit.html")
def doctor_info(request):
    return render(request,"doctor/doctor_info.html")
def doctor_new(request):
    return render(request,"doctor/doctor_new.html")
def doctor_stats(request):
    return render(request,"doctor/doctor_stats.html")
def doctor_table(request):
    return render(request,"doctor/doctor_table.html")
