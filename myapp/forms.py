from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Bus,PassengerDetails,ContactMessage


class RegisterForm(UserCreationForm):
    email = forms.EmailField( required=True)
    phone = forms.CharField(max_length = 15)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = User
        fields = ['username','email','phone','dob','password1','password2']

class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'source', 'destination', 'date', 'time', 'total_seats', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Forces the browser to render a date picker
            'time': forms.TimeInput(attrs={'type': 'time'}),  # Forces the browser to render a time picker
        }

class PassengerDetailsForm(forms.ModelForm):
    class Meta:
        model = PassengerDetails
        fields = ['name', 'phone', 'address', 'age', 'gender']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5})
        }