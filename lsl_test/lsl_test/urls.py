from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Other URL patterns...
    path('', include('lsl_api.urls')),
]