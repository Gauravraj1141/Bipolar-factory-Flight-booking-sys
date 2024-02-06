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
from django.db.models import F


class BookFlightTicket(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        input_json, output_json = request.data, {}
        try:
            output_payload = {}
            user_profile = request.user.id
            flight_number = input_json['flight_number']
            # check the  seat availablity 
            flight_seats = Flight.objects.get(flight_number=flight_number).booked_seats
            if flight_seats >=60:
                output_json = {
                "Status": 200,
                "Message": "all seat have been already booked",
                "Payload": None
                }
                return Response(output_json)


            book_ticket = Booking.objects.create(
                user_id=user_profile, flight_id=flight_number, booking_time=datetime.now())

            output_payload = book_ticket.booking_id

            # update the flight booked seats 
            Flight.objects.filter(flight_number=flight_number).update(booked_seats=F('booked_seats') + 1)

            output_json = {
                "Status": 200,
                "Message": "Flight has been booked successfully",
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
        



