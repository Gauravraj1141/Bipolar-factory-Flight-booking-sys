from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from ...serializers import FlightSerializer, FlightStatus, BookingSerializer
from ...models import Flight, Booking, FlightStatus
from datetime import datetime,timedelta


class RemoveFlight(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    
    def get(self, request,flight_number):
        output_json = {}
        try:
            output_payload = {}
            
            remove_flight = Flight.objects.filter(flight_number=flight_number).delete()

            output_json = {
                "Status": 200,
                "Message": "Flight has been removed successfully",
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