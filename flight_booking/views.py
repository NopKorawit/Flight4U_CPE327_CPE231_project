from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from django.urls import reverse
from flight_booking.models import *
from datetime import datetime
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db.models import Max
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

# ----------------Home page (search)------------------------------------
def search(request):
    city = City.objects.all()
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        departure_date = reFormatDateMMDDYYYY(
            request.POST.get('departure_date'))
        seat_class = request.POST.get('seat_class')
        return render(request, 'search.html', {
            'departure': departure,
            'destination': destination,
            'departure_date': departure_date,
            'seat_class': seat_class,
            'city': city
        })

    else:
        return render(request, "search.html", {
            'min_date': min_date,
            'max_date': max_date,
            'city': city
        })

#-------------------------Get data from search page and go to View flight page--------------

def flight_view(request):
    if request.method=='GET':
        departure = request.GET.get('departure')
        destination = request.GET.get('destination')
        seat_class = request.GET.get('seat_class')
        date = request.GET.get('departure_date')
        departure_date = reFormatDateMMDDYYYY(request.GET.get('departure_date'))
        
        try:
            # print("try to check if departure date is exist in database")
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
    else: 
        print('ERROR!')
        return redirect('/')

#---------------view flight page ------------------
def viewflight(request):
    return render(request, 'view.html')

#------------register and login form------------------
def registerForm(request):
    return render(request, 'register.html')


def loginform(request):
    return render(request, 'loginform.html')

# --------------Add new user (from register page) to database--------------------------

def addUser(request):
    Firstname = request.POST['Firstname']
    Lastname = request.POST['Lastname']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword']

    if password == repassword:
        if User.objects.filter(username=username).exists():
            messages.info(request, "This Username is already used.")
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "This email is already used.")
            return redirect('/register')

        else:
            user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=Firstname,
            last_name=Lastname
            )
            user.save()
            return redirect('/login')
    else:
        messages.info(request, "Password doesn't match.")
        return redirect('/register')

#---------------authenticate user and login--------------------

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Incorrect Username/Password")
            return redirect('/loginform')
    else:
        return render(request, 'loginform.html')

#--------------Logout----------------------------

def logout(request):
    auth.logout(request)
    return redirect('/')


# --------------------Get details from view page (when you choose any flight)-------------------------------

def booking(request,fid,path,date,seat_class):

    booking_detail = Flight.objects.select_related("flight_detail","flight_id","path_id").get(flight_id=fid,flight_detail__departure_date=date, 
                                                    flight_id__seat_class=seat_class,path_id=path)
    duration = booking_detail.duration
    path_id = Travel.objects.filter(path_id=path)
    depart_detail = City_A.objects.filter(city_id=path_id[0].departure)
    desti_detail = City_B.objects.filter(city_id=path_id[0].destination)
    date = reFormatDateMMDDYYYY(date)
    return render(request,'booking.html',{
        'booking_detail' : booking_detail,
        'departure_date' : date,
        'departure' : depart_detail,
        'destination' : desti_detail,
        'duration' : duration
        })


#--------------Add passenger (fill in booking page) after press proceed to payment button---------------

def addPassenger(request):
    if request.method == 'POST':
        flight_id = request.POST['flight_id']
        departure_date = request.POST['departure_date']
        seat_class = request.POST['seat_class']
        total_amount = reFormatNumber(request.POST['total_amount'])
        username = request.POST['username']
        passengerscount = request.POST['passengersCount']
        ticket = createticket(flight_id,departure_date,seat_class,total_amount,username)
        for i in range(1, int(passengerscount)+1): 
            if Passenger.objects.count() != 0:
                id_max = Passenger.objects.aggregate(Max('id'))['id__max']
                next_id = str(int(id_max)+1)
            else:
                next_id = "0"
            id = next_id   
            fname = request.POST[f'fname{i}']
            lname = request.POST[f'lname{i}']
            email = request.POST[f'email{i}']
            phone = request.POST[f'phone{i}']
            id_no = request.POST[f'idno{i}']
            passenger = Passenger.objects.create(
                id=id,
                first_name=fname, 
                last_name=lname, 
                email=email,
                phone_no=phone,
                id_no=id_no,
                ticket_id=ticket,
            )
            passenger.save()
            ticket_id = ticket.ticket_id
            print('ticket:',ticket_id)

        return render(request,'payment.html',{
            'ticket_id':ticket_id,
            'total_amount':total_amount
            })
    
    else:
        return redirect('/')


#-----------in Payment page and response to congratulation page------------------------------------

def confirm(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.status = 'CONFIRMED'
            ticket.booking_date = datetime.now()
            ticket.save()
            return render(request,'confirm.html',{
                'ticket_id': ticket_id
        })
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be post.")


#--------------------create E-ticket, ticket in my booking page and save to database----------------------------------------------------

def createticket(flight_id,departure_date,seat_class,total_amount,username):
        
    if Ticket.objects.count() != 0:
        ticket_id_max = Ticket.objects.aggregate(Max('ticket_id'))['ticket_id__max']
        next_ticket_id = ticket_id_max[0:2] + str(int(ticket_id_max[2:5])+1)
    else:
        next_ticket_id = "TK100"

    status = False
    if status == True:
        status = 'CONFIRMED'
    else: 
        status = 'PENDING'

    ticket_id = next_ticket_id
    date = reFormatDateYYYYMMDD(departure_date)

    print(ticket_id,flight_id,date,seat_class,status)
    ticket = Ticket.objects.create(
            ticket_id=ticket_id,
            flight_id_id=flight_id,
            departure_date=date,
            seat_class=seat_class,
            status=status,
            total_amount=total_amount,
            username =username
            )

    ticket.save()

    return ticket

#---------------my booking page ---------------
def my_booking(request):
    tickets = Ticket.objects.filter(username=request.user.username).order_by('-ticket_id').values('ticket_id','flight_id','departure_date',
                                                                                            'seat_class','total_amount','booking_date','status')
    return render(request, 'my_booking.html', {
        'tickets': tickets,
    })

#----------------------resume pay booking (link to payment's path )--------------------

def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket_id = request.POST['ticket_id']
            ticket = Ticket.objects.get(ticket_id=ticket_id)
            if ticket.username == request.user.username:
                return render(request, "payment.html", {
                    'total_amount': ticket.total_amount,
                    'ticket_id': ticket.ticket_id
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")

#------------Cancle ticket and update status of ticket --------------------

@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket_id = request.POST['ticket_id']
            try:
                ticket = Ticket.objects.get(ticket_id=ticket_id)
                if ticket.username == request.user.username:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                    # return redirect('/my_booking')
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


# -----------------this part is used for ticket details ------------------------------------------------

class TicketPDF(View):
    def get(self, request, pk):
        ticket_id = pk

        ticket = list(Ticket.objects.filter(ticket_id=ticket_id).values('ticket_id','flight_id','departure_date','seat_class','status','username','booking_date'))
        passenger = list(Passenger.objects.filter(ticket_id=ticket_id).order_by('id_no').values("id_no","ticket_id","first_name","last_name","phone_no","email"))
        flight_id = ticket[0]['flight_id']
        flight_detail = list(Flight.objects.select_related("flight_detail","flight_id","path_id").filter(flight_id=flight_id).values(
                                                            'flight_id','airline','path_id__departure','path_id__destination','departure_time',
                                                            'arrival_time','duration'))
        departure_code = flight_detail[0]['path_id__departure']
        destination_code = flight_detail[0]['path_id__destination']
        departure = list(City_A.objects.filter(city_id=departure_code).values('city_id','city_name','airport'))
        destination = list(City_B.objects.filter(city_id=destination_code).values('city_id','city_name','airport'))

        data = dict()
        data['ticket'] = ticket[0]
        data['passenger'] = passenger
        data['flight_detail'] = flight_detail[0]
        data['departure'] = departure[0]
        data['destination'] = destination[0]

        # return JsonResponse(data)
        return render(request, 'ticket.html', data)

#--------------Reformat anything----------------

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[8:10] + "/" + ddmmyyyy[5:7] + "/" + ddmmyyyy[:4]

def reFormatDateYYYYMMDD(yyyymmdd):
    if (yyyymmdd == ''):
            return ''
    return yyyymmdd[6:10] + "-" + yyyymmdd[3:5] + "-" + yyyymmdd[:2]


def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")


def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")


# ------------------LIST--------------------------
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

# -----------------------------------------------------------      

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


