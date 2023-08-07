from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PersonForm
from .models import District, SubDistrict,AccountType
from django.http import JsonResponse


# Create your views here.

def regist(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if User.objects.filter(username=username).exists():
            error_message = "Username already exist.Please choose different username."
            return render(request, "regi.html", {'error_message':error_message})

        if not username or not password or not cpassword:
            error_message = "Please fill in all fields."
            return render(request, "regi.html", {'error_message':error_message})

        if password != cpassword:
            error_message = "Password do not match."
            return render(request,"regi.html", {'error_message':error_message})

        user = User.objects.create_user(username=username, password=password)
        user.save();
        return render(request, "login.html")

    return render(request, "regi.html")


def login(request):
    error_message = ""
    if request.method == 'POST':
        Username = request.POST['username']
        Password = request.POST['password']
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            return render(request, "newpage.html")
        else:
            error_message = "Invalid Username or password."

    return render(request,"login.html", {'error_message': error_message})

def newpage(request):
    return render(request,"newpage.html")


def create_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, 'Application accepted.')
            # return render(request, 'detail.html', {'form': PersonForm(request.GET)})
            return redirect('/')
        else:
            print("Form errors",form.errors)
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = PersonForm()
    return render(request, 'detail.html', {'form': form})


def get_sub_districts(request):
    district_id = request.GET.get('district_id')
    sub_districts = SubDistrict.objects.filter(district_id=district_id).values('id', 'name')
    return JsonResponse({'sub_districts': list(sub_districts)})

def final_page(request):
    return render(request,'final.html')

def logout(request):
        auth.logout(request)
        return redirect('/')

