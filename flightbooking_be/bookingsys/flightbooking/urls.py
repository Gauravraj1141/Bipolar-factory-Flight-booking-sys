from django.urls import path
from flightbooking.apis.simple_user.views_search_flights import SearchFlights
from flightbooking.apis.simple_user.views_book_flight_ticket import BookFlightTicket
from flightbooking.apis.simple_user.views_get_flight_tickets import GetFlightTickets
from flightbooking.apis.simple_user.views_fetch_all_locations import FetchAllLocations

from flightbooking.apis.admin_user.views_add_flights import AddFlight
from flightbooking.apis.admin_user.views_remove_flights import RemoveFlight
from flightbooking.apis.admin_user.views_fetch_all_flights import FetchAllFligths
from flightbooking.apis.admin_user.views_fetch_all_bookings import FetchAllBooking


urlpatterns = [
    path('search_flights/', SearchFlights.as_view(), name="search_flights"),
    path('add_flight/', AddFlight.as_view(), name="add_flight"),
    path('remove_flight/<uuid:flight_number>/', RemoveFlight.as_view(), name="remove_flight"),
    path('book_flight_ticket/', BookFlightTicket.as_view(), name="book_flight_ticket"),
    path('get_flight_tickets/', GetFlightTickets.as_view(), name="get_flight_tickets"),
    path('fetch_all_locations/', FetchAllLocations.as_view(), name="fetch_all_locations"),
    path('fetch_all_flights/', FetchAllFligths.as_view(), name="fetch_all_flights"),
    path('fetch_all_bookings/', FetchAllBooking.as_view(), name="fetch_all_bookings")

]
