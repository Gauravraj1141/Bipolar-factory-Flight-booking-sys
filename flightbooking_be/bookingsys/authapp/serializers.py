from rest_framework import serializers
from .models import CustomUser, UserType

class CustomuserSerializer(serializers.ModelSerializer):
    user_type_name = serializers.ReadOnlyField(source='usertype.type_name')

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "usertype", "user_type_name"]
