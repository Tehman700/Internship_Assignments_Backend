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
    # IF ANYONE WANTS TO TAKE TOKEN ON SEPARATE ENDPOINT NOT ON THE LOGIN ENDPOINT, THEN COMMENT OUT THESE BELOW TWO LINES
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # (Optional) JWT token obtain
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # (Optional) JWT token refresh
]
