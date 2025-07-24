from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blogapp.Views.admin_deletion import admin_deletion
from blogapp.Views.LoginViewSet import LoginViewSet
from blogapp.Views.RegisterViewSet import RegisterViewSet
from blogapp.Views.BlogPostViewSet import BlogPostViewSet

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'blogs', BlogPostViewSet, basename='blogs')

register_view = RegisterViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='custom-register'),
    path('admin_deletion/', admin_deletion, name='admin-deletion'),
]
