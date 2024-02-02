from django.contrib import admin
from django.urls import path, include  # Import the include function

urlpatterns = [
    path('admin/', admin.site.urls),
    # Prefix all API routes with /api/
    path('api/core/', include('core.urls')),  # Include URLs from the core app
    # You can add more apps in a similar manner
    # path('api/another_app/', include('another_app.urls')),
]
