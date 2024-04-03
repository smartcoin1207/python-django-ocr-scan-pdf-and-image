"""
URL mapping for the user API.
"""
from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('ocr/', views.read_from_image, name='read-image'),
    path('process/ocr/', views.process_ocr, name='process-ocr'),
    path('result/<slug:id>/', views.manage_result, name='manage_result'),
    path('results/<slug:history_id>/', views.get_results_by_history, name='get-history-results'),
    path('results/<slug:history_id>/user/<slug:user_id>/', views.get_results_with_history, name='get-results-with-history'),
    path('history/<slug:company_id>/', views.get_history, name='get-history'),
]
