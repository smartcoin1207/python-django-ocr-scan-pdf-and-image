"""
URL mapping for the user API.
"""
from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('ocr/', views.read_from_image, name='read-image'),
]
