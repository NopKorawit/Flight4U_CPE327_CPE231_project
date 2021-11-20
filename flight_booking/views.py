from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
# from .DBHelper import DBHelper
from django.db import connection
from django.urls.conf import path
from flight_booking.models import *
from datetime import datetime
from django.contrib import messages
# from django.contrib.auth import login,authenticate,logout
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, response
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
import json

#Generate account_no

from string import ascii_uppercase
import itertools

def iter_all_strings():
    for size in itertools.count(2):
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)

def noList():
    nolist = []
    for s in iter_all_strings():
        nolist.append(s)
        if s == 'AG':
            break
    return(nolist)

def listID():
    nolist = noList()
    idlist = []
    for no in nolist:
        for i in range(1,100):
            idlist.append(f"{no}{i:02}")
    return(idlist)

def genID():
    for id in listID():
        if not Account.objects.filter(account_no=id).exists():
            break
    return(id)

#--------------------------------------------------------------

def index(request):
    return render(request,'index.html')

def search(request):
    city = City.objects.all()
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        departure_date = reFormatDateMMDDYYYY(request.POST.get('departure_date'))
        seat_class = request.POST.get('seat_class')
        return render(request, 'search.html', {
            'departure': departure,
            'destination': destination,
            'departure_date': departure_date,
            'seat_class': seat_class,
            'city': city
        })
        
    else:
        return render(request,"search.html", {
            'min_date': min_date,
            'max_date': max_date,
            'city': city
        })
    # return render(request,'index.html')
    
def my_booking(request):
    return render(request,'my_booking.html')

def viewflight(request):
    return render(request,'view.html')

# form receive input

def registerForm(request):
    return render(request,'register.html')

def loginform(request):
    return render(request,'loginform.html')

def payment(request):
    return render(request,'payment.html')

def confirm(request):
    return render(request,'confirm.html')

#----------------------------------------------

def addUser(request):
    #account_no = genID()
    Firstname = request.POST['Firstname']
    Lastname = request.POST['Lastname']
 #  phone_no = request.POST['phone_no']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword']

    if password==repassword:
        if User.objects.filter(username=username).exists():
            messages.info(request,"This Username is already used.")
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,"This email is already used.")
            return redirect('/register')
        # elif User.objects.filter(phone_no=phone_no).exists():
        #     messages.info(request,"This phone number is already used.")
        #     return redirect('/register')
        else:
            user = User.objects.create_user(
            #account_no=account_no,
            username=username,
            email=email,
            password=password,
            first_name=Firstname,
            last_name=Lastname
#           phone_no=phone_no,
            )
            user.save()
            return redirect('/login')

    else :
        messages.info(request,"Password doesn't match.")
        return redirect('/register')

# def login(request):
#     email = request.POST['email']
#     password = request.POST['password']
#     #check email and password
#     user = authenticate(email=email,password=password)
#     if not User.objects.filter(email=email).exists():
#         messages.info(request,'this email does not exist')

#     if user is not None: #user is exist
#         messages.info(request,'Login success!')
#         login(request,user)
#         return redirect('/')
#     else: 
#         messages.info(request,'this email does not exist')
#         return redirect('/loginform')

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request, "Incorrect Username/Password")
            return redirect('/loginform')
    else:
        return render(request,'loginform.html')

def logout(request):
    auth.logout(request)
    return redirect('/')




#------------------LIST--------------------------
class CityList(View):
    def get(self,request):
        cities = list(City.objects.all().values())
        data = dict()
        data['cities'] = cities
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class PathList(View):
    def get(self,request):
        paths = list(Travel.objects.all().values())
        data = dict()
        data['paths'] = paths
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class PathDetail(View):
    def get(self, request, id):
        path = list(Travel.objects.select_related("city").filter(path_id=id).values('path_id','departure__city_name','destination__city_name','departure__airport','destination__airport'))
        path_detail = list(Flight.objects.select_related("flight_id").filter(path_id=id).values('flight_id','airline','departure_time','arrival_time','path_id__departure','path_id__destination','flight_id__seat_class'))
        data = dict()
        data['path'] = path[0]
        data['path_detail'] = path_detail

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response


class ClassList(View):
    def get(self, request):
        seat_classes = list(FlightClass.objects.all().values())
        data = dict()
        data['seat_classes'] = seat_classes
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ClassDetail(View):
    def get(self, request, pk):
        seat_class = get_object_or_404(FlightClass, pk=pk)
        data = dict()
        data['seat_classes'] = model_to_dict(seat_class)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#-----------------------------------------------------------      

class FlightList(View):
    def get(self, request):
        flights = list(Flight.objects.order_by('flight_id').all().values())
        data = dict()
        data['flights'] = flights
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class FlightDetail(View):
    def get(self, request, id):
        flight = list(Flight.objects.select_related("flightclass","travel").filter(flight_id=id).values('flight_id','airline','departure_time','arrival_time','path_id__departure','path_id__destination','flight_id__seat_class', 'flight_id__price'))
        flight_detail = list(Flight_Detail.objects.select_related("flight_id").filter(flight_id=id).values('flight_id','departure_date','gate_no'))
        data = dict()
        data['flight'] = flight[0]
        data['flight_detail'] = flight_detail

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

#------------------Fetch part--------------------------


#-----------------ORM ver.------------------------

def flight_view(request):
    if request.method=='GET':
        departure = request.GET.get('departure')
        destination = request.GET.get('destination')
        seat_class = request.GET.get('seat_class')
        date = request.GET.get('departure_date')
        departure_date = reFormatDateMMDDYYYY(request.GET.get('departure_date'))
        
        try:
            #print("try to check if departure date is exist in database")
            flights = Flight.objects.select_related("flight_id","flight_detail").filter(path_id__departure = departure,
                                            path_id__destination=destination,flight_id__seat_class=seat_class,
                                            flight_detail__departure_date=date)
            
            city_a = City_A.objects.filter(city_id=departure)
            city_b = City_B.objects.filter(city_id=destination)
        except:
            print("ERROR!")
            return redirect('/searchflight')
        else:
            
            return render(request,'view.html',{
            'flights' : flights,
            'departure' : city_a[0] ,
            'destination' : city_b[0],
            'seat_class' : seat_class,
            'departure_date': departure_date,
            'date' : date

        })
        

#-------------------------------------------------------------

def booking(request,fid,path,date,seat_class):

    booking_detail = Flight.objects.select_related("flight_detail","flight_id","path_id").get(flight_id=fid,flight_detail__departure_date=date, 
                                                    flight_id__seat_class=seat_class,path_id=path)
    duration = booking_detail.duration
    path_id = Travel.objects.filter(path_id=path)
    depart_detail = City_A.objects.filter(city_id=path_id[0].departure)
    desti_detail = City_B.objects.filter(city_id=path_id[0].destination)
    return render(request,'booking.html',{
        'booking_detail' : booking_detail,
        'departure' : depart_detail,
        'destination' : desti_detail,
        'duration' : duration
        
        })
    #pass

#-------------------------------------------------------
    
def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[8:10] + "/" + ddmmyyyy[5:7] + "/" + ddmmyyyy[:4]


def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]






