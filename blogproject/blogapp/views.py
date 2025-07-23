from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied



class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
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

class LoginViewSet(viewsets.ViewSet):


    def create(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response({"status": 0, "message": "Login successfully", "refresh": str(refresh), "access": str(refresh.access_token)}, status=200)


            else:
                return Response({"status": 1, "message": "Login Failed", "errors" : serializer.errors}, status=200)


        except Exception as e:
            return Response({"status": -1, "message": "Initial Error Occurred", "errors" : str(e)}, status=200)





class IsWriterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        # if for (GET, HEAD, OPTIONS) AS ALL VIEWERS AND READERS CAN VIEW
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated


        # IF FOR OTHER REQUESTS (POST, PUT, DELETE) THEN IT MUST BE WRITER
        return request.user.is_authenticated and request.user.role == 'writer'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user







class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [IsWriterOrReadOnly]


    def get_queryset(self):
        user = self.request.user                                # the particular user
        if user.is_authenticated:                               # if is validated and authenticated, it covers all JWT
            if user.role == 'writer':                           # if writer
                return BlogPost.objects.filter(author=user)     # filter out the object of that user as author = user
            return BlogPost.objects.all()                       # viewer sees all
        return BlogPost.objects.none()                          # return empty if nothing

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": 0,
                "message": "Blog posts fetched successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error in fetching posts",
                "errors": str(e)
            }, status=200)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": 0,
                "message": "Post retrieved successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error retrieving blog post",
                "errors": str(e)
            }, status=200)

    def create(self, request):
        try:
            self.check_permissions(request)
        except PermissionDenied as e:
            return Response({
                "status": 1,
                "message": str(e)
            }, status=200)
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response({
                    "status": 0,
                    "message": "Blog post created",
                    "data": serializer.data
                }, status=200)
            return Response({
                "status": 1,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error during creation",
                "errors": str(e)
            }, status=200)

    def update(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            instance = self.get_object()
            if instance.author != request.user:
                return Response({
                    "status": 1,
                    "message": "You are not allowed to update this post"
                }, status=200)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 0,
                    "message": "Blog post updated",
                    "data": serializer.data
                }, status=200)
            return Response({
                "status": 1,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error during update",
                "errors": str(e)
            }, status=200)

    def destroy(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            instance = self.get_object()
            if instance.author != request.user:
                return Response({
                    "status": 1,
                    "message": "You are not allowed to delete this post"
                }, status=200)

            instance.delete()
            return Response({
                "status": 0,
                "message": "Blog post deleted"
            }, status=200)
        except Exception as e:
            return Response({
                "status": -1,
                "message": "Error deleting blog post",
                "errors": str(e)
            }, status=200)
