"""
URL configuration for gdt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from applicants import views as applicant_views
from schemes import views as scheme_views
from applications import views as application_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/applicants',applicant_views.ApplicantView.as_view()),
    path('api/applicants/<str:nric>/update',applicant_views.ApplicantView.as_view()),
    path('api/schemes',scheme_views.SchemeView.as_view()),
    path('api/schemes/eligible',scheme_views.SchemeEligibilityView.as_view()),
    path('api/applications',application_views.ApplicationView.as_view()),
    path('admin/', admin.site.urls)
]
