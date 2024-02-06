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


class AddFlight(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    
    def post(self, request):
        input_json, output_json = request.data, {}
        try:
            output_payload = {}
            departure_time = input_json['departure_date_time']
            print(departure_time,">>>it is departure time")
            json_data = dict(zip(['departure_time','from_location','to_location','flight_status'],
                                 [departure_time,input_json['from_location'],input_json['to_location'],1]))
            add_flight = FlightSerializer(data =json_data)

            if add_flight.is_valid():
                flight_instance = add_flight.save()
            else:
                print(f"Error: {add_flight.errors}")

            print(add_flight.data,'>>>it it add flight data')
            output_json = {
                "Status": 200,
                "Message": "Flight has been added successfully",
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