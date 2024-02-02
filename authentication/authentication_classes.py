from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions


class LicenseAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        license_code = request.META.get('HTTP_LICENSE_CODE')  # or use request.headers.get('License-Code')
        if not license_code:
            return None  # No attempt made to authenticate because license code is missing

        try:
            user = get_user_model().objects.get(license_code=license_code)
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None  # Authentication successful
