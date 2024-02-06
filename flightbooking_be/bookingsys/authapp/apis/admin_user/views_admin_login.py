from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from ...models import UserType, CustomUser
from rest_framework_simplejwt.tokens import AccessToken

class AdminLoginGenerateToken(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access', None)

            if access_token:
                try:
                    decoded_token = AccessToken(access_token)
                    user = decoded_token.payload
                    user_id = user.get('user_id', None)

                    if user_id:
                        try:
                            user_details = CustomUser.objects.get(pk=user_id)
                            user_type = user_details.usertype.type_id

                            if user_type == 2:
                                custom_response = {
                                    "Status": 200,
                                    "Message": "Login successful.",
                                    "Payload": {
                                        'user_type': user_type,
                                        'user_id': user_id,
                                        'is_admin': True,
                                        'access_token': access_token
                                    }
                                }

                                return Response(custom_response, status=status.HTTP_200_OK)
                            else:
                                return Response({"Status": 403, "Message": "You are not authorized to login"}, status=status.HTTP_403_FORBIDDEN)

                        except UserType.DoesNotExist:
                            pass

                except Exception as e:
                    print(f"Error decoding access token: {e}")

        return response
