"""
Custom permissions for Users app.
"""
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsCampaignManager(permissions.BasePermission):
    """
    Allows access only to campaign managers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_campaign_manager())


class IsVolunteer(permissions.BasePermission):
    """
    Allows access only to volunteers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_volunteer())


class IsAdminOrCampaignManager(permissions.BasePermission):
    """
    Allows access only to admin users or campaign managers.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and
            (user.is_admin() or user.is_campaign_manager())
        )


class IsAdminOrSelf(permissions.BasePermission):
    """
    Allows access only to admin users or the user themselves.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(
            user and user.is_authenticated and
            (user.is_admin() or obj == user)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access only to object owner or admin users.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Check if user is admin
        if user.is_admin():
            return True

        # Check if user is the owner
        if hasattr(obj, 'user'):
            return obj.user == user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == user
        elif hasattr(obj, 'volunteer'):
            return obj.volunteer == user
        elif hasattr(obj, 'owner'):
            return obj.owner == user

        # Default to object equality
        return obj == user