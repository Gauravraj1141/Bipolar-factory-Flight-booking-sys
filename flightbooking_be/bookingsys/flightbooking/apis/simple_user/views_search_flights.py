from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ...serializers import FlightSerializer, FlightStatus, BookingSerializer
from ...models import Flight, Booking, FlightStatus, Location
from datetime import datetime


class SearchFlights(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        input_json, output_json = request.data, {}
        try:
            from_location_id = input_json["from"]
            to_location_id = input_json["to"]
            date_time_str = input_json["date_time"]
            original_date = datetime.fromisoformat(date_time_str[:-1])
            formatted_date_string = original_date.strftime("%Y-%m-%d %H:%M:%S")
            print(formatted_date_string, '>>>>formated')

            get_all_flight = Flight.objects.filter(
                from_location_id=from_location_id,
                to_location_id=to_location_id,
                departure_time__gte=formatted_date_string,
                flight_status_id=1,
                booked_seats__lt=59
            )
            get_all_flight_var = FlightSerializer(
                get_all_flight, many=True).data
            get_all_flight_var = fetch_flight_data(get_all_flight_var)
            
            
            output_payload = get_all_flight_var

            print(get_all_flight_var, '>>all flights data ')
            output_json = {
                "Status": 200,
                "Message": "All available flights are fetched successfully",
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

def fetch_flight_data(flight_data):
    for flights in flight_data:
        from_location = Location.objects.get(
            location_id=flights['from_location'])
        flights['from_location_name'] = from_location.location_name
        to_location = Location.objects.get(
            location_id=flights['to_location'])
        flights['to_location_name'] = to_location.location_name

        # Change the date-time format
        original_datetime_str = flights['departure_time']
        
        original_datetime = datetime.strptime(
            original_datetime_str, "%Y-%m-%dT%H:%M:%S%z")  # Updated format string
        formatted_datetime_str = original_datetime.strftime(
            "%Y-%m-%d %H:%M:%S")
        flights['departure_time'] = formatted_datetime_str
    return flight_data

