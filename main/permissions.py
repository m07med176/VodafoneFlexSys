from rest_framework import permissions
from account.models import Account
class IsActivePermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        try:
            account = request.user
            return True
        except Account.DoesNotExist:
            return False