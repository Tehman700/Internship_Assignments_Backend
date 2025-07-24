from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from blogapp.Serializers.LoginSerializer import LoginSerializer


"""
    Workflow for LoginViewSet:
    - Accepts login credentials (e.g., username/email and password) via POST request.
    - Uses LoginSerializer to validate credentials.
    - If valid:
        - Retrieves the authenticated user.
        - Generates JWT refresh and access tokens using RefreshToken.
        - Returns tokens with status code 0 and success message.
    - If invalid:
        - Returns errors with status code 1 and failure message.
    - If an unexpected error occurs:
        - Returns error message with status code -1.

    Always returns HTTP 200 OK for all cases except URL not found.
"""

class LoginViewSet(viewsets.ViewSet):

    # INTENTIONALLY ADDED THIS SO THAT OTHER REQUEST OTHER THAN POST WILL NOT GET 405 EXCEPTION:
    def dispatch(self, request, *args, **kwargs):
        # Allow only POST requests
        if request.method != 'POST':
            return JsonResponse({
                "status": 1,
                "message": f"Method {request.method} not allowed. Only POST is supported."
            }, status=200)
        return super().dispatch(request, *args, **kwargs)


    def create(self, request):    # Handles POST and Login Requests
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():  #  The validate() method in the LoginSerializer returns a user if valid
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response({"status": 0, "message": "Login successfully", "refresh": str(refresh), "access": str(refresh.access_token)}, status=200)


            else:
                return Response({"status": 1, "message": "Login Failed", "errors" : serializer.errors}, status=200)


        except Exception as e:
            return Response({"status": -1, "message": "Initial Error Occurred", "errors" : str(e)}, status=200)

