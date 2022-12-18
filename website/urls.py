from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='homeView'),

    path('take-test', views.taketest_view, name='taketestView'),

    path('blogs', views.blogs_view, name='blogsView'),
    path('blog/<slug>/read', views.blog_details, name='blogRead'),

    path('doctors', views.doctors_view, name='doctorsView'),
    path('recommended-doctors', views.recommendedDoctors, name='recommendedDoctors'),

    path('contact-us', views.contactus_view, name='contactusView'),

    path('login', views.userLogin_view, name='userLoginView'),
    path('register-user', views.userRegister_form, name='userRegisterForm'),
    path('login-user', views.userLogin_form, name='userLoginForm'),
    path('logout', views.user_logout, name='userLogout'),
]
