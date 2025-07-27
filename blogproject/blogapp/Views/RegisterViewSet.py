from rest_framework import viewsets
"""
Workflow for RegisterViewSet:
- Accepts user data (username, password, role, etc.) via POST request.
- Validates the incoming data using RegisterSerializer.
- If valid:
    - Saves the new user.
    - Returns success response with status code 0 and user data.
- If invalid:
    - Returns error response with status code 1 and serializer validation errors.
- If an unexpected exception occurs:
    - Returns initial error with status code -1 and error message.

Always returns HTTP 200 OK, regardless of success or error,
except for incorrect URL (which would be 404).
"""

class RegisterViewSet(viewsets.ModelViewSet):
    from blogapp.models import User
    queryset = User.objects.all()
    from blogapp.Serializers.RegisterSerializer import RegisterSerializer
    serializer_class = RegisterSerializer       # Used everytime for telling what serializer and queryset using
    http_method_names = ['post']
# INTENTIONALLY ADDED THIS SO THAT OTHER REQUEST OTHER THAN POST WILL NOT GET 405 EXCEPTION:
    def dispatch(self, request, *args, **kwargs):
        # Allow only POST requests
        if request.method != 'POST':
            from django.http import JsonResponse

            return JsonResponse({
                "status": 1,
                "message": f"Method {request.method} not allowed. Only POST is supported."
            }, status=200)
        return super().dispatch(request, *args, **kwargs)



    def create(self, request, *args, **kwargs):

        from django.http import JsonResponse

        if request.method != 'POST':
            return JsonResponse({'error': 'Method must be POST.'}, status=200)
        try:
            from rest_framework.response import Response
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                                    "status": 0,
                                    "message": "Registration successful",
                                    "data": {
                                        "username": user.username,
                                        "email": user.email,
                                        "role": user.role
                                    }
                                }, status=200)


            else:
                return Response({
                            "status": 1,
                            "message": "Registration failed",
                            "errors": serializer.errors
                        }, status=200)
        except Exception as e:
                    return Response({
                        "status": -1,
                        "message": "Initial error occurred",
                        "errors": str(e)
                    }, status=200)