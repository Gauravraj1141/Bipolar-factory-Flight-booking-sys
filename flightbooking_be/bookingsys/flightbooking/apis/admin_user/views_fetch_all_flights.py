from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ...serializers import FlightSerializer, FlightStatus, BookingSerializer
from ...models import Flight, Booking, FlightStatus
from datetime import datetime, timedelta
from flightbooking.apis.simple_user.views_search_flights import fetch_flight_data


class FetchAllFligths(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        output_json = {}
        try:

            fetch_all_flights = Flight.objects.all()
            flight_serializer = FlightSerializer(
                fetch_all_flights, many=True).data
            output_payload = fetch_flight_data(flight_serializer)

            output_json = {
                "Status": 200,
                "Message": "all flights fetched successfully",
                "Payload": output_payload
            }
            return Response(output_json)
        except Exception as e:
            output_json = {
                "Status": 500,
                "Message": f"Some Error occured Exception is {e}",
                "Payload": None
            }
            return Response(output_json)
