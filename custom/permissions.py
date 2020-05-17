from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsSenderOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not isinstance(obj.sender, User):
            return False
        return obj.sender == request.user


class IsReceiverOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not isinstance(obj.receiver, User):
            return False
        return obj.receiver == request.user


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not isinstance(obj.creator, User):
            return False
        return obj.creator == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, User):
            return obj == request.user
        if isinstance(obj.user, User):
            return obj.user == request.user
        return False
