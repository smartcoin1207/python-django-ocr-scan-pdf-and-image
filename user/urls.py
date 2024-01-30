"""
URL mapping for the user API.
"""
from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    # path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('password/forgot/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/reset/', views.PasswordResetView.as_view(), name='reset_password'),
    path('google/', views.get_or_create_user, name='get_user'),
]
