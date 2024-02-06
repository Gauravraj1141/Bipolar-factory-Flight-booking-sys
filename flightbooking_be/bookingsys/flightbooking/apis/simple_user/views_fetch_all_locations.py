from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from ...serializers import FlightSerializer, FlightStatus, BookingSerializer,LocationSerializer
from ...models import Flight, Booking, FlightStatus, Location

class FetchAllLocations(APIView):

    def get(self, request):
        output_payload = {}
        
        all_locations = Location.objects.all()
        all_locations_var = LocationSerializer(all_locations, many=True).data
        output_payload = all_locations_var
        output_json = {
            "Status": 200,
            "Message": "Locations are fetched successfully",
            "Payload": output_payload
        }
        return Response(output_json)
    
    