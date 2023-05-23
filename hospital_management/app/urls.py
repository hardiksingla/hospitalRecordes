from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("login/", views.login),
    path("signup/", views.signup),
    path("logout/", views.logout),
    path("userpage/",views.userpage),
    path("user_table",views.user_table),
    path("user_stats",views.user_stats),
    path("user_new",views.user_new),
    path("user_info",views.user_info),
    path("user_table",views.user_table),
    path("user_table",views.user_table),
    
    path("doctor/",views.doctor)
]