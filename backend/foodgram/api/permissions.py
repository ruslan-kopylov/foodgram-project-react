from rest_framework import permissions


class AuthenticatedForObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated


class AuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
