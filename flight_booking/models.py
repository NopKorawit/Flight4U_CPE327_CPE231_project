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
        return self.city_id

class Flight(models.Model):
    flight_id = models.CharField(max_length=5,primary_key=True)
    airline = models.CharField(max_length=20)
    departure = models.CharField(max_length=5) #city_id
    destination = models.CharField(max_length=5) #city_id
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):
        return self.flight_id,self.airline


class Account(models.Model):
    account_no = models.CharField(max_length=10, primary_key=True) # id card/passport nunmber 
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=10)
    card_no = models.CharField(max_length=20)
    

    class Meta:
        db_table = "account"
        managed = False
    def __str__(self):
        return self.account_no

# class FlightDetail(models.Model):
#     flight_id = models.CharField(max_length=5,primary_key=True)
#     depart_date = models.DateField()
#     gate_no = models.CharField(max_length=5)

#     class Meta:
#         db_table = "flight_detail"
#         unique_together = (("flight_id", "depart_date"),)
#         managed = False
#     def __str__(self):
#         return '{"flight_id":"%s","depart_date":"%s","gate_no":"%s"}' % (self.flight_id, self.depart_date, self.gate_no)
