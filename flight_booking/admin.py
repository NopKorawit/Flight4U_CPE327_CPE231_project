from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(City)
admin.site.register(FlightClass)
admin.site.register(Flight)
admin.site.register(Flight_Detail)
admin.site.register(Ticket)
admin.site.register(Passenger)
admin.site.register(Payment)