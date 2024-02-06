from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ...serializers import FlightSerializer, FlightStatus, BookingSerializer
from ...models import Flight, Booking, FlightStatus
from flightbooking.apis.simple_user.views_search_flights import fetch_flight_data


class GetFlightTickets(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        output_payload = {}

        get_all_tickets = Booking.objects.filter(user_id=request.user.id)
        get_all_tickets_var = BookingSerializer(
            get_all_tickets, many=True).data
        for tickets in get_all_tickets_var:
            flight_id = tickets['flight']
            flight_detail = Flight.objects.filter(pk=flight_id)
            flight_detail_var = FlightSerializer(flight_detail, many=True).data
            tickets['flight_detail'] = fetch_flight_data(flight_detail_var)

        output_payload = get_all_tickets_var

        output_json = {
            "Status": 200,
            "Message": "All flights tickets are fetched successfully",
            "Payload": output_payload
        }
        return Response(output_json)
