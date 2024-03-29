from rest_framework import permissions


class IsAuthAdminUserOrAuthReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class CanViewHistory(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')
