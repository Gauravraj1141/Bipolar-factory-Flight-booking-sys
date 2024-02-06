from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from ...models import UserType, CustomUser
from ...serializers import CustomuserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,IsAdminUser

class FetchUserProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # input_json, output_payload = request.data, {}
        try:

            profile = CustomUser.objects.filter(pk=request.user.id)
            profile_serializer_var = CustomuserSerializer(profile, many=True).data

            output_json = {
                "Status": 200,
                "Message": "User details fetch Successfully",
                "Payload": profile_serializer_var
            }
            return Response(output_json)
        except Exception as e:
            output_json = {
                "Status": 404,
                "Message": "Some Problem Occured in user profile"
            }
            return Response(output_json)