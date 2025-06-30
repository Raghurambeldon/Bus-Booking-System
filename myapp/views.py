from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .forms import RegisterForm,BusForm,PassengerDetailsForm,ContactForm
from .models import UserProfile,Bus,Seat,Booking,PassengerDetails
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods,require_POST
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
# Create your views here.
@login_required
def home(request):
    return render(request,'home.html')

#admin/super users addbus through form
@user_passes_test(lambda user: user.is_superuser)
def addbus_view(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save()

            for i in range(1, bus.total_seats + 1):
                Seat.objects.create(bus=bus, number=i)
                messages.info(request,"Bus Created Successfully . . .")
            return redirect('addbus')  
    else:
        form = BusForm()

    return render(request, 'add_bus.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            UserProfile.objects.create(user=user, phone=phone, dob=dob)
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(data = request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request,user)
        return redirect('buslist')
    
    return render(request,'login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')

def buslist_view(request):
    now = datetime.now()
    buses = Bus.objects.filter(date__gt=now.date()).order_by('date','time')
    return render(request,'buslist.html',{'buses':buses})


def seats_view(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    seats = Seat.objects.filter(bus_id=bus_id).order_by('number')
    return render(request, 'seatsview.html', {'bus': bus, 'seats': seats,'bus_id':bus_id})



@login_required
@require_http_methods(["GET", "POST"])
def book_seat(request, bus_id, seat_id):
    seat = get_object_or_404(Seat, id=seat_id, bus_id=bus_id)


    if request.method == 'GET':
        # Show confirmation and payment page
        return render(request, 'passenger_details.html', {'seat': seat})

    elif request.method == 'POST':
      seat.is_booked = True
      seat.save()

    Booking.objects.create(user=request.user, bus=seat.bus, seat=seat,status = 'Confirmed')

    return render(request, 'bookingsuccessful.html', {'seat': seat})



@login_required
def mybookings_view(request):
    user = request.user
    mybookings = Booking.objects.filter(user=user).order_by('-booked_at')

    # Create a dictionary: booking.id -> passenger
    passenger_map = {}

    for booking in mybookings:
        try:
            passenger = PassengerDetails.objects.get(
                user=user,
                bus=booking.bus,
                seat=booking.seat
            )
            passenger_map[booking.id] = passenger
        except PassengerDetails.DoesNotExist:
            passenger_map[booking.id] = None

    return render(request, 'mybookings.html', {
        'mybookings': mybookings,
        'passengers': passenger_map  # Pass as dict
    })


@login_required
@require_POST
def cancel_booking(request, booking_id):
    # Get the booking object or return a 404 error if it doesn't exist
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Ensure the booking belongs to the current user
    if booking.user == request.user:
        # Update the booking status to 'Cancelled'
        booking.status = 'Cancelled'
        
        # Unbook the seat by setting is_booked to False
        seat = booking.seat
        seat.is_booked = False
        seat.save()  # Save the seat's updated status

        # Save the updated booking status
        booking.save()

    # After canceling the booking, redirect to the "mybookings" page
    return redirect('mybookings')

@login_required
def passenger_details_view(request, seat_id, bus_id):
    seat = get_object_or_404(Seat, id=seat_id)
    bus = get_object_or_404(Bus, id=bus_id)

    if seat.is_booked:
        return render(request, 'error.html', {'message': 'This seat is already booked.'})

    if request.method == 'POST':
        form = PassengerDetailsForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.user = request.user
            passenger.bus = bus
            passenger.seat = seat
            passenger.save()

            # ✅ Save info in session (defer actual booking)
            request.session['passenger_id'] = passenger.id
            request.session['seat_id'] = seat.id
            request.session['bus_id'] = bus.id

            return redirect('confirm_payment')
    else:
        form = PassengerDetailsForm()

    return render(request, 'passenger_details.html', {
        'form': form,
        'seat': seat,
        'bus': bus
    })



@login_required
def confirm_payment(request):
    passenger_id = request.session.get('passenger_id')
    seat_id = request.session.get('seat_id')
    bus_id = request.session.get('bus_id')

    if not all([passenger_id, seat_id, bus_id]):
        return redirect('home')

    passenger = get_object_or_404(PassengerDetails, id=passenger_id)
    seat = get_object_or_404(Seat, id=seat_id)
    bus = get_object_or_404(Bus, id=bus_id)

    if request.method == 'POST':
        # Mark the seat as booked
        seat.is_booked = True
        seat.save()

        # Create booking (no passenger link since your model doesn't have it)
        Booking.objects.create(
            user=request.user,
            bus=bus,
            seat=seat,
            status='Confirmed'
        )

        # Clear session
        request.session.pop('passenger_id', None)
        request.session.pop('seat_id', None)
        request.session.pop('bus_id', None)

        return redirect('mybookings')

    return render(request, 'confirm_payment.html', {
        'seat': seat,
        'bus': bus,
        'passenger': passenger
    })

@login_required
def contactus_view(request):
    submitted = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact-us/?submitted=True')  # Adjust this if your URL is different
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contactus.html', {
        'form': form,
        'submitted': submitted
    })

#SEArCh bus


def searchthebus(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query_origin = request.GET.get('origin', '')
        query_dest = request.GET.get('destination', '')

        buses = Bus.objects.filter(
            Q(source__icontains=query_origin),
            Q(destination__icontains=query_dest)
        )

        results = []
        for bus in buses:
            results.append({
                'id': bus.id,
                'name': bus.name,
                'source': bus.source,
                'destination': bus.destination,
                'date': bus.date.strftime('%Y-%m-%d'),
                'time': bus.time.strftime('%H:%M'),
                'price': str(bus.price)
            })

        return JsonResponse({'buses': results})
    
    return render(request, 'searchthebus.html')


