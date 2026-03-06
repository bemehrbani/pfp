"""
Serializers for Users app.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User
from apps.analytics.models import ActivityLog


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'telegram_id', 'telegram_username', 'telegram_chat_id',
            'phone_number', 'points', 'level', 'email_verified', 'phone_verified',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'points', 'level', 'email_verified', 'phone_verified',
            'created_at', 'updated_at'
        )


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'role')
        extra_kwargs = {
            'role': {'required': False}
        }

    def validate(self, data):
        """Validate password confirmation."""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': _('Passwords do not match.')})

        # Default role to volunteer if not specified
        if 'role' not in data or not data['role']:
            data['role'] = User.Role.VOLUNTEER

        # Only admins can create other admins or campaign managers
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if data['role'] in [User.Role.ADMIN, User.Role.CAMPAIGN_MANAGER]:
                if not request.user.is_admin():
                    raise serializers.ValidationError(
                        {'role': _('Only admins can create users with this role.')}
                    )
        else:
            # New registration from anonymous user - only allow volunteer
            if data['role'] != User.Role.VOLUNTEER:
                raise serializers.ValidationError(
                    {'role': _('New registrations can only create volunteer accounts.')}
                )

        return data

    def create(self, validated_data):
        """Create a new user with hashed password."""
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(_('User account is disabled.'))
                data['user'] = user
            else:
                raise serializers.ValidationError(_('Unable to log in with provided credentials.'))
        else:
            raise serializers.ValidationError(_('Must include "username" and "password".'))

        return data


class TelegramLinkSerializer(serializers.Serializer):
    """Serializer for linking Telegram account."""
    telegram_id = serializers.IntegerField()
    telegram_username = serializers.CharField(max_length=32, required=False, allow_blank=True)
    telegram_chat_id = serializers.IntegerField(required=False)

    def validate_telegram_id(self, value):
        """Check if Telegram ID is already linked to another user."""
        if User.objects.filter(telegram_id=value).exclude(id=self.context['user'].id).exists():
            raise serializers.ValidationError(_('This Telegram account is already linked to another user.'))
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user role."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = self.user

        # Create login activity log
        ActivityLog.objects.create(
            user=user,
            action_type=ActivityLog.ActionType.USER_LOGIN,
            description=f'User {user.username} logged in',
            content_object=user
        )

        return validated_data