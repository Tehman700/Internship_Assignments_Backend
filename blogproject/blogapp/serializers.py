from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


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


      # Below two lines are just for checking thought maybe we can use it later
      #  validated_data['password'] = make_password(validated_data['password'])  # hash password
      #  return super().create(validated_data)




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




"""
For the BlogPost Serializer, the author field was to be fetched from source and others are just normally same as we
import from Meta class the Model name is BlogPost in the model.py file and the other required fields

"""




class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'publication_date', 'author']
