from rest_framework import serializers
from blogapp.models import User

"""
For the Register Serializer, the Password field is for the authentication and since we are using User model so we defined
this in the Meta class and other fields which are necessary for Registering,
The def create function will be only called when the data is validated and we will create a new user specially with this data

"""

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'mobile_number', 'role', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

#       Below two lines are just for checking thought maybe we can use it later
#        validated_data['password'] = make_password(validated_data['password'])  # hash password