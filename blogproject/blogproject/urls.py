from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blogapp.Urls.urls')),  # ✅ this is good now
]
