from django.shortcuts import redirect, render
from django.http import HttpResponse

from .DBHelper import DBHelper
from flight_booking.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login,authenticate

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
# Create your views here.

def index(request):
    return render(request,'index.html')

def search(request):
    city = City.objects.all
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        destination = request.POST.get('Destination')
        depart_date = request.POST.get('DepartDate')
        seat = request.POST.get('SeatClass')
        trip_type = request.POST.get('TripType')
        if(trip_type == '1'):
            return render(request, 'search.html', {
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'city': city
        })
        elif(trip_type == '2'):
            return_date = request.POST.get('ReturnDate')
            return render(request, 'search.html', {
            'min_date': min_date,
            'max_date': max_date,
            'origin': origin,
            'destination': destination,
            'depart_date': depart_date,
            'seat': seat.lower(),
            'trip_type': trip_type,
            'return_date': return_date,
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

#----------------------------------------------

def addUser(request):
    account_no = genID()
    email = request.POST['email']
    phone_no = request.POST['phone_no']
    card_no = request.POST['card_no']
    password = request.POST['password']
    repassword = request.POST['repassword']

    if password==repassword:
        if Account.objects.filter(email=email).exists():
            messages.info(request,"This email is already used.")
            return redirect('/register')
        elif Account.objects.filter(phone_no=phone_no).exists():
            messages.info(request,"This phone number is already used.")
            return redirect('/register')
        elif Account.objects.filter(card_no=card_no).exists():
            messages.info(request,"This card number is already used.")
            return redirect('/register')
        else:
            account = Account.objects.create(
                account_no=account_no,
                email=email,
                password=password,
                phone_no=phone_no,
                card_no=card_no )
            account.save()
            messages.info(request,"Register success!")
            return redirect('/')

    else :
        messages.info(request,"Password doesn't match.")
        return redirect('/register')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    #check email and password
    user = authenticate(email=email,password=password)
    if not Account.objects.filter(email=email).exists():
        messages.info(request,'this email does not exist')

    if user is not None: #user is exist
        messages.info(request,'Login success!')
        login(request,user)
        return redirect('/')
    else: 
        messages.info(request,'this email does not exist')
        return redirect('/loginform')


    
