"""
URL configuration for core project.

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
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from members.views import editUserProfil, me, allUsers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('categories.urls')),
    path('api/', include('books.urls')),
    path('api/', include('authors.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('members.urls')),
    path('api/users/editUserProfil', editUserProfil),
    path('api/users/me', me),
    path('api/users/', allUsers)
]
    

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)