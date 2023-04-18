"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from APP.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('import/', import_data, name='import'),
    path('Qualification/', Qualification, name='Qualification'),
    path('Repeatability/', Repeatability, name='Repeatability'),
    path('Predict/', Predict, name='Predict'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

