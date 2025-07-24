from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .urls import *


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
    queryset = User.objects.all()
    serializer_class = RegisterSerializer       # Used everytime for telling what serializer and queryset using
    http_method_names = ['post']

# INTENTIONALLY ADDED THIS SO THAT OTHER REQUEST OTHER THAN POST WILL NOT GET 405 EXCEPTION:
    def dispatch(self, request, *args, **kwargs):
        # Allow only POST requests
        if request.method != 'POST':
            return JsonResponse({
                "status": 1,
                "message": f"Method {request.method} not allowed. Only POST is supported."
            }, status=200)
        return super().dispatch(request, *args, **kwargs)



    def create(self, request, *args, **kwargs):

        if request.method != 'POST':
            return JsonResponse({'error': 'Method must be POST.'}, status=200)
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
    permission_classes = []



# Normally we use builtin queryset for fetching all the users, but we have some restrictions so created separate function
    def get_queryset(self):
        user = self.request.user                                # the particular user
        if user.is_authenticated:                               # if is validated and authenticated, it covers all JWT
            if user.role == 'writer':                           # if writer
                return BlogPost.objects.filter(author=user)     # filter out the object of that user as author = user
            return BlogPost.objects.all()                       # viewer sees all
        return BlogPost.objects.none()                          # return empty if nothing



# The above function just gets the raw queryset to view it we use below function

    def list(self, request):  # Called when GET /api/blogs/
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)  # Converts to list of dictionaries
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




# Retrieve function is called when we want to get specific id or blogpost with id
    def retrieve(self, request, *args, **kwargs):  # GET /api/blogs/<id>/
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





    def create(self, request, *args, **kwargs):
        # Check custom permission manually to control the response
        permission = IsWriterOrReadOnly()
        if not permission.has_permission(request, self):
            return Response({
                "status": 1,
                "message": "You are not allowed, you are a viewer"
            }, status=status.HTTP_200_OK)

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=False)

            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response({
                    "status": 0,
                    "message": "Blog post created",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "status": 1,
                "message": "Validation failed",
                "errors": serializer.errors
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": -1,
                "message": "Unexpected error during creation",
                "errors": str(e)
            }, status=status.HTTP_200_OK)




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

            # If correct user
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



    from .permissions import IsViewer

    @action(detail=True, methods=['post'], url_path='like', permission_classes=[IsViewer])
    def like(self, request, pk=None):
        blog_post = self.get_object()
        serializer = BlogReactionSerializer(
            data={'reaction_type': 'like'},
            context={'request': request, 'blog_post': blog_post}
        )
        serializer.is_valid(raise_exception=True)
        reaction = serializer.save()
        toggled_off = serializer.context.get('toggled_off', False)

        message = "Like removed" if toggled_off else "Liked successfully"
        return Response({
            "status": 0,
            "message": message,
            "data": BlogReactionSerializer(reaction).data if not toggled_off else {}
        }, status=200)

    @action(detail=True, methods=['post'], url_path='dislike', permission_classes=[IsViewer])
    def dislike(self, request, pk=None):
        blog_post = self.get_object()
        serializer = BlogReactionSerializer(
            data={'reaction_type': 'dislike'},
            context={'request': request, 'blog_post': blog_post}
        )
        serializer.is_valid(raise_exception=True)
        reaction = serializer.save()
        toggled_off = serializer.context.get('toggled_off', False)

        message = "Dislike removed" if toggled_off else "Disliked successfully"
        return Response({
            "status": 0,
            "message": message,
            "data": BlogReactionSerializer(reaction).data if not toggled_off else {}
        }, status=200)




    @action(detail=True, methods=['post'], url_path='comment', permission_classes=[IsViewer])
    def comment(self, request, pk=None):
        blog_post = self.get_object()
        serializer = BlogCommentSerializer(
            data=request.data,
            context={'request': request, 'blog_post': blog_post}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": 0, "message": "Comment added", "data": serializer.data}, status=200)







# This is a seperate Code for working when admin wants to delete all the Posts and everything from database
# Using a Harcoded Username and Password
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db import connection
from .models import BlogPost

User = get_user_model()

@csrf_exempt
def admin_deletion(request):
    if request.method != 'POST':
        return JsonResponse({"status": 1, "message": "Only POST allowed"}, status=200)

    try:
        body = json.loads(request.body)
        username = body.get("username")
        password = body.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"status": -1, "message": "Invalid JSON body"}, status=200)

    # Hardcoded credentials
    admin_username = "admin123"
    admin_password = "deleteEverything"

    if username != admin_username or password != admin_password:
        return JsonResponse({"status": 1, "message": "Invalid admin credentials"}, status=200)

    try:
        # Delete all blog posts and users
        BlogPost.objects.all().delete()
        User.objects.all().delete()

        # Reset auto-increment ID counters for blog posts and users
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='blogapp_blogpost'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='blogapp_user'")

        return JsonResponse({
            "status": 0,
            "message": "All blog posts and users deleted. IDs reset to 1."
        }, status=200)

    except Exception as e:
        return JsonResponse({
            "status": -1,
            "message": "Unexpected error during deletion",
            "errors": str(e)
        }, status=200)

