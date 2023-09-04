from rest_framework import permissions


class IsBrandManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a brand manager.
        return request.user.is_authenticated and request.user.is_brand_manager