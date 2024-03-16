"""
URL mapping for the user API.
"""
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/', views.PasswordResetView.as_view(), name='reset_password'),
    path('google/', views.get_or_create_user, name='get_user'),
    path('<slug:user_id>/company/<slug:company_id>/', views.get_company_users, name='get_users'),
    path('new/', views.create_new_user, name='create_user'),
    path('<slug:id>/', views.manage_user, name='manage_user'),
]
