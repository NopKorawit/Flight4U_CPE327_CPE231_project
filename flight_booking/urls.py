from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_booking",views.my_booking),
    path("searchflight",views.search),
    path("register",views.registerForm),
    path("viewflight",views.flight_view),
    path("addUser",views.addUser),
    path("loginform",views.loginform),
    path("login",views.login),
    path("logout",views.logout),
    path("<str:id>/<str:seat_class>",views.booking),
    path("payment",views.payment),

    # path('receipt/list', views.FlightList.as_view(), name='receipt_list'),
    # path('receipt/detail/<str:id>', views.FlightDetail.as_view(), name='receipt_detail'),

    

]