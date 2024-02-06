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
from authapp.models import CustomUser
from flightbooking.apis.simple_user.views_search_flights import fetch_flight_data


class FetchAllBooking(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        input_json, output_json = request.data, {}
        try:

            fetch_all_bookings = Booking.objects.filter(flight = input_json['flight_number'])
            bookings_serializer = BookingSerializer(
                fetch_all_bookings, many=True).data
            for data in bookings_serializer:
                user_data = data['user']
                customer_data = CustomUser.objects.get(id=user_data)
                data['user_name'] = f"{customer_data.first_name} {customer_data.last_name}"
                data['user_email'] = customer_data.email
                flight_number = data['flight']
                fligth_details = Flight.objects.filter(
                    flight_number=flight_number)
                fligth_details_var = FlightSerializer(
                    fligth_details, many=True).data
                data['flight_details'] = fetch_flight_data(fligth_details_var)

            output_json = {
                "Status": 200,
                "Message": "all booking fetched successfully",
                "Payload": bookings_serializer
            }
            return Response(output_json)
        except Exception as e:
            output_json = {
                "Status": 500,
                "Message": f"Some Error occured Exception is {e}",
                "Payload": None
            }
            return Response(output_json)


def change_datetime_format(str):
    original_datetime_str = str
    original_datetime = datetime.strptime(
        original_datetime_str, "%Y-%m-%dT%H:%M:%S%z")  # Updated format string
    formatted_datetime_str = original_datetime.strftime(
        "%Y-%m-%d %H:%M:%S")
    return formatted_datetime_str
