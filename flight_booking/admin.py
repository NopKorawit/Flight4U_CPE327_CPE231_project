from django.contrib import admin
from .models import Account, City, Flight, Passenger

# Register your models here.

admin.site.register(Passenger)
admin.site.register(City)
admin.site.register(Account)
admin.site.register(Flight)