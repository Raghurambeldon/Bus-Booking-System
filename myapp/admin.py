from django.contrib import admin
from .models import  Bus,Seat,Booking,UserProfile,PassengerDetails,ContactMessage

# Register your models here.
class Businfo(admin.ModelAdmin):
    list_display = ['name','source','destination','date','time','total_seats','price']


admin.site.register(Bus,Businfo)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(PassengerDetails)
admin.site.register(ContactMessage)


