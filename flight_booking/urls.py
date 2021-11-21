from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("my_booking",views.my_booking),
    path("",views.search),
    path("register",views.registerForm),
    path("viewflight",views.flight_view),
    path("addUser",views.addUser),
    path("loginform",views.loginform),
    path("login",views.login),
    path("logout",views.logout),
<<<<<<< HEAD
    path("<str:fid>&<str:path>&<str:date>&<str:seat_class>",views.booking),
    path('addPassenger',views.addPassenger),
    path('payment',views.payment),
=======
    path("booking/<str:fid>&<str:path>&<str:date>&<str:seat_class>",views.booking),
    path("payment",views.payment),
    path("confirm",views.confirm),
>>>>>>> e825dab8bc60a5baaafc7d3a3e2250dba33a3daf

    path('city/list',views.CityList.as_view(),name='city_list'),
    path('flight/list', views.FlightList.as_view(), name='flight_list'),
    path('flight/detail/<str:id>', views.FlightDetail.as_view(), name='flight_detail'),
    path('path/list', views.PathList.as_view(), name='path_list'),
    path('path/detail/<str:id>', views.PathDetail.as_view(), name='path_detail'),
    path('class/list',views.ClassList.as_view(),name='class_list'),
    path('class/detail/<str:id>', views.ClassDetail.as_view(), name='class_detail'),

    path('ticket/list', views.TicketList.as_view(), name='Ticket_List'),
    path('ticket/detail/<str:pk>', views.TicketDetail.as_view(), name='Ticket_detail'),
    path('ticket/pdf/<str:pk>', views.TicketPDF.as_view(), name='Ticket_pdf'),


    # path('flight/ticket/api/<str:ref>', views.TicketList, name="ticketdata"),
    # path('ticket/print',views.get_ticket, name="getticket"),
    

]