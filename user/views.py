"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token as DefaultTokenModel
from django.contrib.auth.hashers import make_password
from core.models import User
from django.utils.crypto import get_random_string
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from user.serializers import GoogleUserSerializer, UserSerializer, AuthTokenSerializer, TokenSerializer

def get_token_response(user):
    serializer_class = TokenSerializer
    token, _ = DefaultTokenModel.objects.get_or_create(user=user)
    serializer = serializer_class(instance=token)
    return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return get_token_response(user)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ForgotPasswordView(APIView):
    """Send email for restting password."""
    reset_secret = get_random_string(length=32)

    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
            user.reset_password_secret = self.reset_secret
            user.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            send_mail(
                f'パスワード再設定通知（{settings.WEB_SITE_NAME}）',
                f'{settings.WEB_SITE_NAME}用のパスワード再設定はこちらから {settings.RESET_PASSWORD_URL}{self.reset_secret}',
                settings.SENDER_EMAIL,
                [request.data['email']],
                fail_silently=False,
            )
        except BadHeaderError:
            return Response('Invalid header found')
        return Response(status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """Reset password of user."""
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(reset_password_secret=request.data['reset_secret'])
            user.password = make_password(request.data['password'])
            user.reset_password_secret = None
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_or_create_user(request):
    email = request.data.get("email", None)
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email)
        user.save()
    serializer = GoogleUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)



