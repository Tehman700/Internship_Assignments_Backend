from rest_framework import serializers
from blogapp.models import User


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