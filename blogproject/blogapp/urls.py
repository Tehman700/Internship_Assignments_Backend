from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet, RegisterViewSet, BlogPostViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
#router.register(r'users', UserViewSet, basename='user')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'blogs', BlogPostViewSet, basename='blogs')

register_view = RegisterViewSet.as_view({'post': 'create'})

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='custom-register'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
