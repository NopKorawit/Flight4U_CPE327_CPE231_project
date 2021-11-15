from django.db import models

# Create your models here.

class Passenger(models.Model):
    id_no = models.CharField(max_length=20, primary_key=True) # id card/passport nunmber 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=10)
    email = models.CharField(max_length=30)

    class Meta:
        db_table = "passenger"
        managed = False
    def __str__(self):
        return self.id_no

class City(models.Model):
    city_id = models.CharField(max_length=5,primary_key=True)
    city_name = models.CharField(max_length=50)

    class Meta:
        db_table = "city"
        managed = False
    def __str__(self):
        return self.city_id,self.city_name

class Account(models.Model):
    username = models.CharField(max_length=10, primary_key=True) # id card/passport nunmber 
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "account"
        managed = False
    def __str__(self):
        return self.username


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
    departure = models.CharField(max_length=5) #city_id
    destination = models.CharField(max_length=5) #city_id
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    
    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):
        return self.flight_id


class FlightDetail(models.Model):
    flight_id = models.CharField(max_length=5,primary_key=True)
    departure_date = models.DateField()
    gate_no = models.CharField(max_length=5)

    class Meta:
        db_table = "flight_detail"
        unique_together = (("flight_id", "departure_date"),)
        managed = False
    def __str__(self):
        return '{"flight_id":"%s","departure_date":"%s","gate_no":"%s"}' % (self.flight_id, self.departure_date, self.gate_no)
