from django.urls import path
from . import views

urlpatterns = [
    # auth routes
    path('login', views.login_view, name='loginView'),
    path('logined', views.login_form, name='loginForm'),
    path('logout', views.logout_admin, name='adminLogout'),

    # dashboard routes
    path('home', views.dashboard_view, name='dashboardView'),
    path('home/user-delete', views.adminDeleteUser, name="adminDeleteUser"),

    # doctor routes
    path('add-doctor', views.addDoctor_view, name='addDoctorView'),
    path('added-doctor', views.addDoctor_form, name='addDoctorForm'),
    path('all-doctors', views.allDoctors_view, name='allDoctorsView'),
    path('doctor/<id>/details', views.doctorDetails_view, name='doctorDetailsView'),
    path('doctor/delete', views.deleteDoctor, name='deleteDoctor'),
    path('doctor/<id>/edit', views.editDoctor_view, name="editDoctorView"),
    path('udpate-doctor', views.updateDoctor_form, name='updateDoctorForm'),

    # blogs routes
    path('all-blogs', views.allBlogs_view, name='allBlogsView'),
    path('add-blog', views.addBlog_view, name='addBlogView'),
    path('added-blog', views.addBlog_form, name='addBlogForm'),
    path('delete-blog', views.deleteBlog, name='deleteBlog'),


    # inquiries routes
    path('inquiries', views.inquiries_view, name='inquiriesView'),
    path('inquiries/<id>/details', views.inquiriesDetail_view, name='inquiriesDetailView'),
    path('inquiries/<id>/delete', views.deleteInquirie, name='deleteInquirie'),

]
