from django.contrib.auth.models import User

from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        request.user = User.objects.get(username='Julien')
        return bool(request.user
                    and request.user.is_authenticated)
