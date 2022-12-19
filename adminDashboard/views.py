from ctypes.wintypes import PINT
import os
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import doctor_detail
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.files.images import get_image_dimensions
from website.models import inquiries
from .models import blogs

def dashboard_view(request):
    if 'adminEmail' in request.session:
        dr_count = doctor_detail.objects.all().count()
        unread_messege_count = inquiries.objects.filter(status=0).count()
        user_count = User.objects.filter(is_superuser=0).count()
        users = User.objects.filter(is_superuser=0).all()

        context = {
            'dr_count': dr_count,
            'unread_messege_count': unread_messege_count,
            'user_count': user_count,
            'users': users 
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('loginView')

def adminDeleteUser(request):
    user_id = request.POST.get("id")
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('dashboardView')

def login_view(request):
    if 'adminEmail' in request.session:
        return redirect('dashboardView')
    return render(request, 'adminlogin.html')

def login_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_len = len(password)

        if email != "" and password != "": 
            if password_len > 4:

                adminEmail = User.objects.filter(email=email, is_superuser=1).last()
                if adminEmail:
                    matchPasword = check_password(password, adminEmail.password)
                    if matchPasword:
                        request.session['adminEmail'] = email
                        return redirect('dashboardView')
                    else:
                        messages.error(request, "Incorrect Password")
                        return redirect('loginView')
                else:
                    messages.error(request, "Incorrect Email")
                    return redirect('loginView')
            else:
                messages.error(request, "Password must be greater than 4 characters")
                return redirect('loginView')
                
        else:
            messages.error(request, "Email and Password are required Fields")
            return redirect('loginView')
            

    return redirect('loginView')

def logout_admin(request):
    if 'adminEmail' in request.session:
        del request.session['adminEmail']
        return redirect('loginView')
    else:
        return redirect('loginView')

def addDoctor_view(request):
    if 'adminEmail' in request.session:
        return render(request, 'adddoctor.html')
    else:
        return redirect('loginView')
    

def allDoctors_view(request):
    if 'adminEmail' in request.session:
        doctors = doctor_detail.objects.all()
        context={
            'doctors': doctors,
        }
        return render(request, 'alldoctors.html', context)
    else:
        return redirect('loginView')

def addDoctor_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        houspital = request.POST.get('houspital')
        specialization = request.POST.get('specialization')
        meeting_link = request.POST.get('meeting_link')
        services = request.POST.get('tags')
        doctorPicture = request.FILES.get('doctor_picture')


        width, height = get_image_dimensions(doctorPicture)

        if width == 350 and height == 350:
            if name == "" or email == "" or phone == "" or houspital == "" or specialization == "" or services == "" or doctorPicture == "" or meeting_link == "":
                messages.error(request, "All Fields are Required")
                return redirect('addDoctorView')
            else:
                check_email = doctor_detail.objects.filter(email=email).last()
                if check_email:
                    messages.error(request, "Doctor with this email already registered")
                    return redirect('addDoctorView')
                else:
                    data = doctor_detail.objects.create(name=name, email=email, phoneNumber=phone, houspitalName=houspital,
                                            specialization=specialization, services=services, doctorPicture=doctorPicture, meeting_link=meeting_link)
                    data.save()
                    messages.success(request, "Doctor Added")
                    return redirect('addDoctorView')
        else:
            messages.error(request, f"image Dimentions must be 350 x 350, your picture dimentions are {width} x {height}.")
            return redirect('addDoctorView')
        

    return redirect('addDoctorView')


def doctorDetails_view(request, id):
    if 'adminEmail' in request.session:
        doctorDetails = doctor_detail.objects.filter(id=id).last()
        services = doctorDetails.services
        res = eval(services)
        
        context = {
            'doctor': doctorDetails,
            'res': res
        }
        return render(request, 'doctordetails.html', context)
    else:
        return redirect('loginView')


def deleteDoctor(request):
    if request.method == "POST":
        id = request.POST.get('id')
        record = doctor_detail.objects.get(id=id)
        record.delete()
        return redirect('allDoctorsView')
    return redirect('allDoctorsView')
    

def editDoctor_view(request, id):
    doctor_data = doctor_detail.objects.filter(id=id).last()
    context ={
        'doctor': doctor_data,
    }
    return render(request, 'editdoctor.html', context)

def updateDoctor_form(request):
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        houspital = request.POST.get('houspital')
        specialization = request.POST.get('specialization')
        services = request.POST.get('tags')
        doctorPicture = request.FILES.get('doctor_picture')
        meeting_link = request.POST.get('meeting_link')
        print(meeting_link)

        doctor = doctor_detail.objects.filter(id=id).last()

        if name == "" or email == "" or phone == "" or houspital == "" or specialization == "" or services == "" or meeting_link=="" :
            messages.error(request, "No field can be Null")
            return redirect('editDoctorView', id)
        else:
            if doctorPicture:
                width, height = get_image_dimensions(doctorPicture)
                if width == 350 and height == 350:
                    doctor_detail.objects.filter(id=id).update(name=name, email=email, phoneNumber=phone, houspitalName=houspital,
                    specialization=specialization, services=services, meeting_link=meeting_link)

                    os.remove(doctor.doctorPicture.path)
                    doctor.doctorPicture = doctorPicture
                    doctor.save()
                    return redirect('doctorDetailsView', id)
                    
                else:
                    messages.error(request, f"image Dimentions must be 350 x 350, your picture dimentions are {width} x {height}.")
                    return redirect('editDoctorView', id)
            else:
                doctor_detail.objects.filter(id=id).update(name=name, email=email, phoneNumber=phone, houspitalName=houspital,
                specialization=specialization, services=services, meeting_link=meeting_link)
                return redirect('doctorDetailsView', id)       
    return redirect('allDoctorsView')


def inquiries_view(request):
    if 'adminEmail' in request.session:
        data = inquiries.objects.all()
        context = {
            'data': data,
        }
        return render(request, 'inquiries.html', context)
    else:
        return redirect('loginView')


def inquiriesDetail_view(request, id):
    if 'adminEmail' in request.session:
        message = inquiries.objects.filter(id=id).last()
        inquiries.objects.filter(id=id).update(status=1)
        context = {
            'message': message,
        }
        return render(request, "readmessage.html", context)
    else:
        return redirect('loginView')    


def deleteInquirie(request, id):
    inquiries.objects.filter(id=id).delete()
    return redirect('inquiriesView')


def allBlogs_view(request):
    if 'adminEmail' in request.session:
        blog = blogs.objects.all()
        context = {
            'blogs' : blog,
        }
        return render(request, "allblogs.html", context)
    else:
        return redirect('loginView')  

def addBlog_view(request):
    if 'adminEmail' in request.session:
        return render(request, "addblog.html")
    else:
        return redirect('loginView')  

def addBlog_form(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('blog_content')
        thumbnail = request.FILES.get('blog_thumbnail')

        if title == "" or content == "" or thumbnail == "":
            messages.error(request, "All feilds are required")
            return redirect('addBlogView')
        else:
            slug = title.replace(" ", "-")
            querry = blogs.objects.create(title=title, content=content, thumbnail=thumbnail, slug=slug)   
            querry.save()
            messages.success(request, "Blog Added Successfully")
            return redirect('addBlogView')

def deleteBlog(request):
    if request.method == "POST":
        id = request.POST.get('id')
        blog = blogs.objects.get(id=id)
        blog.delete()
        return redirect('allBlogsView')




    
