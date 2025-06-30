from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bus(models.Model):
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField( max_length=100)
    date = models.DateField()
    time = models.TimeField()
    total_seats = models.IntegerField(default=60)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)

    def __str__(self):
        return f"{self.name} | {self.source} --> {self.destination} on {self.date} "
    

class Seat(models.Model):
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    number = models.CharField(max_length=8)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.number} on {self.bus.name}"
    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled')
    )


    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE)
    booked_at = models.DateTimeField( auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')

    def __str__(self):
        return f"{self.user.username} booked {self.seat.number} on {self.bus.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    dob = models.DateField()


    def __str__(self):
        return self.user.username
    


class PassengerDetails(models.Model):
    STATUS_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'bus', 'seat')

    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"