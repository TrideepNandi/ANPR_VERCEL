from rest_framework import permissions


class IsHOD(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'hod'


class IsDirector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'director'


class IsManagement(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'management'


class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'operator'


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'user'
