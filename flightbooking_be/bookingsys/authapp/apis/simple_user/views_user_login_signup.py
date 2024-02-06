from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from ...models import UserType, CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class UserSignup(APIView):
    """
    {
    "username": "DrSachins",
    "email_id": "sachsin@mailinator.com",
    "password": "sachin321r",
    "first_name": null,
    "last_name": null
    }
    """

    def post(self, request):
        input_json, output_payload = request.data, {}
        try:

            plaintext_password = input_json['password']
            hashed_password = make_password(plaintext_password)

            user_signup = CustomUser.objects.create(
                username=input_json['username'],
                email=input_json['email_id'],
                password=hashed_password,
                first_name=input_json['first_name'],
                last_name=input_json['last_name'],
                usertype_id=1,
            )
            output_payload = user_signup.username

            output_json = {
                "Status": 200,
                "Message": "Signup successful. Please proceed to log in.",
                "Payload": output_payload
            }
            return Response(output_json)
        except Exception as e:
            output_json = {
                "Status": 404,
                "Message": "The chosen username is already in use"
            }
            return Response(output_json)



class CustomTokenObtainForUser(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access', None)

            if access_token:
                from rest_framework_simplejwt.tokens import AccessToken

                try:
                    decoded_token = AccessToken(access_token)
                    user = decoded_token.payload
                    user_id = user.get('user_id', None)

                    if user_id:
                        try:
                            userdetails = CustomUser.objects.get(pk=user_id)
                            user_type = userdetails.usertype.type_id
                            
                            if user_type == 1:
                                custom_response = {
                                    "Status": 200,
                                    "Message": "Login successful.",
                                    "Payload": {
                                        'user_type': user_type,
                                        'user_id': user_id,
                                        'is_admin': False,
                                        'access_token':access_token
                                    }
                                }
                                
                                return Response(custom_response, status=status.HTTP_200_OK)
                            else:
                                return Response({"Status": 404, "Message": "You are not able to login"}, status=status.HTTP_404_NOT_FOUND)
                                
                        except UserType.DoesNotExist:
                            pass

                except Exception as e:
                    print(f"Error decoding access token: {e}")

        return response