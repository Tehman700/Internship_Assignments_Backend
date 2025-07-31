from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blogapp.Views.LoginViewSet import LoginViewSet
from blogapp.Views.RegisterViewSet import RegisterViewSet
from blogapp.Views.BlogPostViewSet import BlogPostViewSet
from blogapp.Utils.admin_deletion import admin_deletion

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')      # Handles user login (POST)
router.register(r'blogs', BlogPostViewSet, basename='blogs')   # CRUD for blog posts

register_view = RegisterViewSet.as_view({'post': 'create'})    # Custom route for user registration
urlpatterns = [
    path('', include(router.urls)),                             # Includes login/ and blogs/ endpoints
    path('register/', register_view, name='custom-register'),  # POST only - user registration
    path('admin_deletion/', admin_deletion, name='admin-deletion'),
    path('comments/<int:comment_id>/like/', BlogPostViewSet.as_view({'post': 'like_comment'}), name='like-comment'),
    path('comments/<int:comment_id>/dislike/', BlogPostViewSet.as_view({'post': 'dislike_comment'}),name='dislike-comment'),
]