from rest_framework import authentication, permissions

from django.conf import settings


class HasApiPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        api_key = request.META.get("HTTP_API_KEY")
        print(request.META)
        print("HasApiPermission", api_key, settings.API_TOKEN)

        if api_key == settings.API_TOKEN:
            return True

        return False
