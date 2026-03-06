"""
API views for Users app.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from ..models import User
from ..serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    TelegramLinkSerializer, CustomTokenObtainPairSerializer
)


class RegisterView(generics.CreateAPIView):
    """Register a new user."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Set user as inactive until email verification if required."""
        user = serializer.save()
        # TODO: Send email verification if email is provided
        return user


class LoginView(TokenObtainPairView):
    """Login view using JWT tokens."""
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update current user profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """List users (admin only)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-created_at')
    filterset_fields = ['role', 'is_active']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a user (admin only)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class TelegramLinkView(APIView):
    """Link Telegram account to current user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TelegramLinkSerializer(
            data=request.data,
            context={'user': request.user}
        )
        if serializer.is_valid():
            user = request.user
            user.telegram_id = serializer.validated_data['telegram_id']
            user.telegram_username = serializer.validated_data.get('telegram_username', '')
            user.telegram_chat_id = serializer.validated_data.get('telegram_chat_id')
            user.save(update_fields=[
                'telegram_id', 'telegram_username', 'telegram_chat_id'
            ])
            return Response(
                {'message': _('Telegram account linked successfully.')},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout view - blacklist refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': _('Successfully logged out.')},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {'error': _('Invalid token.')},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    """Change user password."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {'error': _('Both old and new password are required.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {'error': _('Old password is incorrect.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {'error': _('New password must be at least 8 characters long.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {'message': _('Password changed successfully.')},
            status=status.HTTP_200_OK
        )