from rest_framework import serializers
from django.contrib.auth import authenticate

"""
For the Login Serializer, only two fields required one username and other password and we use builtin function
validate to authenticate the incoming user using authenticate() method and user is valid and is active then return
otherwise make sure to defined that its invalid

"""




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError("Invalid Credentials")


