# This is a seperate Code for working when admin wants to delete all the Posts and everything from database
# Using a Harcoded Username and Password
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db import connection
from blogapp.Models.BlogPost import BlogPost

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

    # Hardcoded credentials so that it can be used when deletion of all posts
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