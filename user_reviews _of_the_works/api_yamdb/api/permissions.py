from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """Для аутентифицированных пользователей имеющих статус администратора или
    автора"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class IsAdmin(BasePermission):
    """Только для аутентифицированных пользователей имеющих статус
    администратора или суперюзера."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Для аутентифицированных пользователей имеющих статус администратора """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)
