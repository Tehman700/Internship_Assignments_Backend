from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from blogapp.Serializers.LoginSerializer import LoginSerializer

class LoginViewSet(viewsets.ViewSet):

    # INTENTIONALLY ADDED THIS PART SO THAT OTHER REQUEST OTHER THAN POST WILL NOT GET 405 EXCEPTION:
    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({
                "status": 1,
                "message": f"Method {request.method} not allowed. Only POST is supported."
            }, status=200)
        return super().dispatch(request, *args, **kwargs)

    def create(self, request):  # Handles POST and Login Requests
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data  # This returns the user object from `validate()`

                refresh = RefreshToken.for_user(user)
                entered_password = request.data.get('password')

                return Response({
                    "status": 0,
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "password": entered_password,
                        "email": user.email,
                        "mobile_number": user.mobile_number,
                        "role": user.role,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    },
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),

                }, status=200)
            else:
                return Response({
                    "status": 1,
                    "message": "Login failed",
                    "errors": serializer.errors
                }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Initial error occurred",
                "errors": str(e)
            }, status=200)