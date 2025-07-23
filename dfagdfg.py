# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#
# class LoginViewSet(viewsets.ViewSet):
#     def create(self, request):
#         try:
#             serializer = LoginSerializer(data=request.data)
#             if serializer.is_valid():
#                 username = serializer.validated_data['username']
#                 return Response({
#                     "status": 0,
#                     "message": "Login successful",
#                     "data": f"<h1>Welcome {username}</h1>"
#                 }, status=200)
#             else:
#                 return Response({
#                     "status": 1,
#                     "message": "Login failed",
#                     "errors": serializer.errors
#                 }, status=200)
#         except Exception as e:
#             return Response({
#                 "status": -1,
#                 "message": "Initial error occurred",
#                 "errors": str(e)
#             }, status=200)
#
# class RegisterViewSet(viewsets.ViewSet):
#     def create(self, request):
#         try:
#             serializer = RegisterSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.save()
#                 return Response({
#                     "status": 0,
#                     "message": "Registration successful",
#                     "data": {
#                         "username": user.username,
#                         "email": user.email,
#                         "role": user.role
#                     }
#                 }, status=200)
#             else:
#                 return Response({
#                     "status": 1,
#                     "message": "Registration failed",
#                     "errors": serializer.errors
#                 }, status=200)
#         except Exception as e:
#             return Response({
#                 "status": -1,
#                 "message": "Initial error occurred",
#                 "errors": str(e)
#             }, status=200)
#