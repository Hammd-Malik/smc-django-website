from django.shortcuts import render, redirect, HttpResponse
from adminDashboard.models import doctor_detail
from django.http import JsonResponse
from .models import inquiries
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from adminDashboard.models import blogs

# from .detection_model.chat_bot import *


# Create your views here.
def home_view(request):
    blog = blogs.objects.all()[:3]
    context = {
        'blogs': blog,
    }
    return render(request ,'home.html', context)

def userLogin_view(request):
    if "user" in request.session:
        return redirect('homeView')
    else:
        return render(request, "login.html")

def userRegister_form(request):
    if request.POST.get('action'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        encrypted_password = make_password(password)
        if name == "" or email == "" or password == "":
            messages.error(request, "All fields are required")
            return JsonResponse({'message': "All Fields are Required"})
        else:
            alreadyUser = User.objects.filter(email=email).last()
            username = User.objects.filter(username=name).last()

            if alreadyUser:
                return JsonResponse({'message': "Account already exist for this email"})
            else:
                if username:
                    return JsonResponse({'message': "Select the Unique User name"})
                else:
                    user = User.objects.create(username=name, email=email, password=encrypted_password)
                    user.save()
                    return JsonResponse({'message': "your account is created, login now"})

    return JsonResponse({'message': "Submit the form properly"})

def userLogin_form(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_len = len(password)

        if email == "" or password == "":
            messages.error(request, "All Fields are required")
            return redirect("userLoginView")
            if password_len  < 5:
                messages.error(request, "Password muct be greater then 5 characters")
                return redirect("userLoginView")
        else:
            user = User.objects.filter(email=email).last()
            if user:
                if user.check_password(password):
                    request.session['user'] = user.username
                    request.session['email'] = email
                    login(request, user)
                    return redirect("taketestView")
                else:
                    messages.error(request, "Invalid Password") 
                    return redirect('userLoginView')
            else:
                messages.error(request, "Invalid Email") 
                return redirect('userLoginView')
    messages.error(request, "Submit the Form Properly") 
    return redirect('userLoginView')

def user_logout(request):
    del request.session['user']
    del request.session['email']
    logout(request)
    return redirect("homeView")

# def userSetting_view(request):
#     return render(request, "user-setting.html")

@login_required(login_url="userLoginView")
def taketest_view(request):
    return render(request ,'taketest.html')

def blogs_view(request):
    blog =  blogs.objects.all()
    context = {
        'blogs': blog,
    }
    return render(request ,'blogs.html', context)

def blog_details(request, slug):
    blog = blogs.objects.filter(slug=slug)
    recent_blogs = blogs.objects.all().order_by('-id')[:4]
    context = {
        'blog' : blog,
        'rblogs': recent_blogs,
    }
    return render(request ,'blog-details.html', context)

def doctors_view(request):
    doctors = doctor_detail.objects.all()
    context = {
        'doctors': doctors
    }
    return render(request ,'doctors.html', context)

def recommendedDoctors(request):
    if request.method == "POST":
        disease = request.POST.get('disease')
        recDr = doctor_detail.objects.filter(services__contains=disease)
        context = {
            'doctors' : recDr,
        } 
    return render(request ,'recommended-doctors.html',context)


    
def contactus_view(request):
    if request.POST.get('action') == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = inquiries.objects.create(name=name, email=email, subject=subject, message=message)
        data.save()

    return render(request ,'contact-us.html')


 