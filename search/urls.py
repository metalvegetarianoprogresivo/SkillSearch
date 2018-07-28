"""
mapsapp URL Configuration
"""
from django.urls import path
from .views import *

urlpatterns = [
    path(r'', search, name='search')
]
