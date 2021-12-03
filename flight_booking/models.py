from django.db import models
import datetime
from django.contrib.auth.models import User

from django.db.models import fields

# Create your models here.
    
#Departure
class City_A(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name
#Destination
class City_B(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name
#----------------------------------------------------------------

class City(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)
    airport = models.TextField()
    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_name

#----------------------------------------------------------------
class Travel(models.Model):
    path_id = models.CharField(max_length=5,primary_key=True)
    departure = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)
    class Meta:
        db_table = "travel"
        managed = False
    def __str__(self):
        return self.path_id

class FlightClass(models.Model):
    flight_id = models.CharField(max_length=5,primary_key=True)
    seat_class = models.CharField(max_length=10)
    price = models.IntegerField()
    class Meta:
        db_table = "flight_class"
        unique_together = (("flight_id", "seat_class"),)
        managed = False
    def __str__(self):
        return str(self.flight_id)

class Flight(models.Model):
    flight_id = models.ForeignKey(FlightClass, primary_key=True, on_delete=models.CASCADE, db_column='flight_id')
    airline = models.CharField(max_length=20)
    path_id = models.ForeignKey(Travel, on_delete=models.CASCADE, db_column='path_id')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.TimeField()
    
    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):
        return str(self.flight_id)


class Flight_Detail(models.Model):
    flight_id = models.ForeignKey(Flight, primary_key=True, on_delete=models.CASCADE, db_column='flight_id')
    departure_date = models.DateField()
    gate_no = models.CharField(max_length=5)

    class Meta:
        db_table = "flight_detail"
        unique_together = (("flight_id", "departure_date"),)
        managed = False
    def __str__(self):
        return '{"flight_id":"%s","departure_date":"%s","gate_no"}' % (self.flight_id,self.departure_date,self.gate_no)

#-------------------------------------------------------------------------------
class Ticket(models.Model):
    ticket_id = models.CharField(max_length=10, primary_key=True)
    flight_id = models.ForeignKey(Flight_Detail, on_delete=models.CASCADE, db_column='flight_id')
    departure_date = models.DateField()
    seat_class = models.CharField(max_length=10)
    total_amount = models.FloatField()
    booking_date = models.DateTimeField(blank=True,null=True)
    username = models.CharField(max_length=150)
    status = models.CharField(max_length=10)
    class Meta:
        db_table = "ticket"
        managed = False
    def __str__(self):
        return self.ticket_id

class Passenger(models.Model):
    id = models.IntegerField(primary_key=True)
    id_no = models.CharField(max_length=20) # id card/passport nunmber 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='ticket_id')
    class Meta:
        db_table = "passenger"
        managed = False
    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name} {self.email}"

#-------------------------------------------------------------------------------

