from django.urls import path
from . import views

urlpatterns = [
    path("", views.login),
    path("login/", views.login),
    path("signup", views.signup),
    path("logout/", views.logout),

    path("userpage/",views.userpage),
    path("user_table/",views.user_table),
    path("user_new/",views.user_new),
    path("user_info/",views.user_info),
    path("user_info_edit/",views.user_info_edit),
    path("user_table_info/", views.user_table_info),

    path("doctor/",views.doctor),
    path("doctor_info_edit/",views.doctor_info_edit),
    path("doctor_info/",views.doctor_info),
    path("doctor_new/",views.doctor_new),
    path("doctor_table/",views.doctor_table),
    path("patient_info/", views.patient_info),
    path("patient_info_edit/", views.patient_info_edit),

    path("about/", views.about),
    path("contact/", views.contact)
]