from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .DBHelper import DBHelper
from flight_booking.models import *
from datetime import datetime
from django.contrib import messages
# from django.contrib.auth import login,authenticate,logout

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
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        return render(request, 'search.html', {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'city': city
        })
        
    else:
        return render(request,"search.html", {
            'min_date': min_date,
            'max_date': max_date,
            'city': city
        })
    return render(request,'index.html')
    
def my_booking(request):
    return render(request,'my_booking.html')

def viewflight(request):
    return render(request,'view.html')

# form receive input

def registerForm(request):
    return render(request,'register.html')

def loginform(request):
    return render(request,'loginform.html')

def booking_ticket(request):
    return render(request,'booking_ticket.html')

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
            messages.success(request, f" Hello {username}, You Are Successfully Logged In")
            return redirect('/')
        else:
            messages.info(request, "Incorrect Username/Password")
        return redirect('/loginform')
    else:
        return render(request,'/loginform')

#------------------Fetch part--------------------------

def flight_view(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT f.flight_id as "Flight", f.airline as "Airline", '
                            'f.departure as "Departure", f.destination as "Destination",'
                            'f.departure_time as "Departure Time", f.arrival_time as "Arrival Time",'
                            'f.arrival_time-f.departure_time as "Duration" '
                            'FROM flight f ORDER BY f.flight_id '
                            ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'view.html', data_report)

#-------------------------------------------------------
    
def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result



