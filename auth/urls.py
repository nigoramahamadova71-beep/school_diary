"""
URL configuration for auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from my_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegistrationAPIView.as_view(), name='registration'),
    path('api/login/', LoginAPIView.as_view(), name = 'login'),
    path('api/user-info/', GetInfoUser.as_view(), name = 'info'),
    path('api/user-info/update/', UpdateProfileAPIView.as_view(), name = 'update'),
    path('api/schedule/', GetSchedule.as_view(), name = 'schedule'),
    path('api/grades/', GetGrades.as_view(), name = 'grades'),
    path('api/attendance/', GetAttendance.as_view(), name = 'attendance'),
    path('api/payment/', GetPayment.as_view(), name = 'payment'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
