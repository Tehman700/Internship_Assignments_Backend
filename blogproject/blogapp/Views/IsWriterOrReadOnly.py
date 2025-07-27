from rest_framework import permissions

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
