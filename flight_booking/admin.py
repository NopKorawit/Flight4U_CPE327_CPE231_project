from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Passenger)
# admin.site.register(City_A)
# admin.site.register(City_B)
admin.site.register(City)
admin.site.register(Booking)
admin.site.register(Flight)