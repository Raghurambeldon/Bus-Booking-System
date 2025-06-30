from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [ path('',views.home,name='home'),
               path('bus-list',views.buslist_view,name = 'buslist'),
                path('register/',views.register_view,name='register'),
                path('login/',views.login_view,name='login'),
                path('logout/',views.logout_view,name='logout'),
                path('seats/<int:bus_id>',views.seats_view,name='seatsview'),
              path('book/<int:bus_id>/<int:seat_id>', views.book_seat, name='book_seat'),
              path('my-bookings/',views.mybookings_view,name='mybookings'),
              path('add-bus/',views.addbus_view,name='addbus'),
              path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
              path('passenger-details/<int:seat_id>/<int:bus_id>/', views.passenger_details_view, name='passenger_details'),
             path('contact-us/', views.contactus_view, name='contactus'),
                 path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
                 path('search-the-bus/', views.searchthebus, name='searchthebus'),
]


urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
