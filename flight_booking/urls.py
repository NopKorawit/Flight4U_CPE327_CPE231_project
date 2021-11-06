from typing import ValuesView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_booking",views.my_booking),
    path("searchyourflight",views.search),
    path("register",views.registerForm),
    path("viewflight",views.flight_view),
    path("addUser",views.addUser),
    path("loginform",views.loginform),
    path("login",views.login),
    # path("testflightlist",views.allflight)
    

]