from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import CustomUser, doctorsMore, patient, hospitalMore


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

    elif request.user.is_authenticated:
        if request.user.type == "hospital":
            return redirect("/userpage")
        else:
            return redirect("/doctor")
        
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        add = request.POST["address"]
        username = request.POST['username']
        password = request.POST['pass']
        email = request.POST['email']
        pno = request.POST['pno']
        altpno = request.POST['altpno']

        if CustomUser.objects.filter(username = username).exists():
            messages.info(request, "Username exists")
            return redirect("/signup")
        elif CustomUser.objects.filter(email = email).exists():
            messages.info(request, "Email exists")
            return redirect("/signup")
        elif CustomUser.objects.filter(pno = pno).exists():
            messages.info(request, "Phone number already registered")
            return redirect("/signup")
        elif hospitalMore.objects.filter(altpno = pno).exists():
            messages.info(request, "Alternate Phone number already registered")
            return redirect("/signup")
        
        user = CustomUser(username = username, email = email, pno = pno, first_name = name)
        user.set_password(password)
        user.save()
        more = hospitalMore(hospital = user, altpno = altpno, address = add)
        more.save()
        messages.info(request, "Signup successful")
        return redirect("/login")
    else:
        return render(request, "signup.html")
    
def logout(request):
    auth.logout(request)
    return redirect("/login")

def userpage(request):
    return render(request,"hospital/userpage.html")

def user_table_info(request):
    if request.method == "POST":
        requested = request.POST["requested"]
        curr_doc = doctorsMore.objects.filter(doctor_id = requested).first()
        return render(request,"hospital/user_table_info.html", context={"doctor": curr_doc})

def user_table(request):
    doctors = doctorsMore.objects.filter(hospital = request.user)
    print(doctors)
    return render(request,"hospital/user_table.html", context={"doctors": doctors})

def user_new(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        age = request.POST["age"]
        dob = request.POST["dob"]
        pno = request.POST["phone1"]
        altpno = request.POST["phone2"]
        speciality = request.POST["speciality"]
        degree = request.POST["degree"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        gender = request.POST["gender"]
        
        user = CustomUser(username = username, first_name = fname, last_name = lname, pno = pno, email = email, type = "doctor")
        user.set_password(password)
        user.save()
        more = doctorsMore(doctor = user, altpno = altpno, speciality = speciality, degree = degree, dob = dob, gender = gender, hospital = request.user)
        more.save()
        return redirect('/user_table')
    return render(request,"hospital/user_new.html")

def user_info(request):
    hospital = hospitalMore.objects.filter(hospital = request.user).first()
    print(hospital)
    return render(request,"hospital/user_info.html", context = {"hospital": hospital})

def user_info_edit(request):
    hospital_more = hospitalMore.objects.filter(hospital = request.user).first()
    hospital = hospital_more.hospital

    if request.method == "POST":
        check = 0
        if hospital.first_name != request.POST["name"]:
            hospital.first_name = request.POST["name"]
            check = 1
        if hospital.pno != request.POST["pno"]:
            hospital.pno = request.POST["pno"]
            check = 1
        if hospital.email != request.POST["email"]:
            hospital.email = request.POST["email"]
            check = 1
        if hospital_more.address != request.POST["address"]:
            hospital_more.address = request.POST["address"]
            check = 1       

        password = request.POST["password"]
        if password != "":
            hospital.set_password(password)
            hospital.save()
            hospital_more.save()
            return redirect("/login")
        
        if check == 1:
            hospital.save()
            hospital_more.save()
            return redirect("/user_info")
        
        return redirect("/user_info")
    
    return render(request, "hospital/user_info_edit.html", context={"hospital": hospital_more})



def doctor(request):
    return render(request,"doctor/doctorpage.html")

def doctor_info_edit(request):

    if request.method == "POST":
        curr_patient = patient.objects.filter(id = request.POST["ID_old"]).first()
        values = ["first_name", "last_lname", "dob", "pno", "altpno", "degree", "specialty", "email", "gender"]
        matches = {}
    for i in values:
        new = request.POST[i]
        old = request.POST[i + "_old"]
        if new != old:
            matches[i] = new

    print(matches)
    for i in matches:
        if i == values[0]:
            curr_patient.fname = matches[i]
        elif i == values[1]:
            curr_patient.lname = matches[i]
            print("Last name changed")
        elif i == values[2]:
            curr_patient.dob = matches[i]
        elif i == values[3]:
            curr_patient.pno = matches[i]
        elif i == values[4]:
            curr_patient.diagnosis = matches[i]
        elif i == values[5]:
            curr_patient.prescription = matches[i]
        elif i == values[6]:
            curr_patient.email = matches[i]
        elif i == values[7]:
            curr_patient.gender = matches[i]
    
    print(curr_patient)
    curr_patient.save()
    return redirect("/doctor_table")

def doctor_info(request):
    if request.method == "POST":
        doc_id = request.POST["requested"]
        more_info = doctorsMore.objects.filter(doctor_id = doctor).first()
        return render(request,"doctor/doctor_info.html", context={"more": more_info})

    more_info = doctorsMore.objects.filter(doctor = request.user).first()
    return render(request,"doctor/doctor_info.html", context={"more": more_info})

def doctor_new(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['age']
        pno = request.POST['phone1']
        email = request.POST['email']
        gender = request.POST["gender"]
        diagnosis = request.POST["diagnosis"]
        pres = request.POST["prescription"]

        new_patient = patient(doctor = request.user, fname = fname, lname = lname, dob = dob, pno = pno, email = email, gender = gender, diagnosis = diagnosis, prescription = pres)
        new_patient.save()
        return redirect('/doctor_table')

    return render(request,"doctor/doctor_new.html")

def doctor_table(request):
    patients = patient.objects.filter(doctor = request.user)
    print(patients)
    return render(request,"doctor/doctor_table.html", context={"patients": patients})

def patient_info(request):
    if request.method == "POST":
        requested = request.POST["requested"]
        curr_patient = patient.objects.filter(id = requested).first()
        return render(request,"doctor/patient_info.html", context={"patient": curr_patient})
    
def patient_info_edit(request):

    if request.method == "POST":
        print(request.user)
        curr_patient = patient.objects.filter(id = request.POST["ID_old"]).first()
        values = ["fname", "lname", "dob", "pno", "diagnosis", "prescription", "email", "gender"]
        matches = {}
        for i in values:
            new = request.POST[i]
            old = request.POST[i + "_old"]
            if new != old:
                matches[i] = new

        print(matches)
        for i in matches:
            if i == values[0]:
                curr_patient.fname = matches[i]
            elif i == values[1]:
                curr_patient.lname = matches[i]
                print("Last name changed")
            elif i == values[2]:
                curr_patient.dob = matches[i]
            elif i == values[3]:
                curr_patient.pno = matches[i]
            elif i == values[4]:
                curr_patient.diagnosis = matches[i]
            elif i == values[5]:
                curr_patient.prescription = matches[i]
            elif i == values[6]:
                curr_patient.email = matches[i]
            elif i == values[7]:
                curr_patient.gender = matches[i]
        
        print(curr_patient)
        curr_patient.save()
        return redirect("/doctor_table")

    requested = request.GET["requested"]
    curr_patient = patient.objects.filter(id = requested).first()
    dob = curr_patient.dob.strftime('%Y-%m-%d')
    return render(request,"doctor/patient_info_edit.html", context={"patient": curr_patient, "dob": dob})


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")