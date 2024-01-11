from rest_framework.views import APIView


class CustomAPIView(APIView):
    """
        This class add the permissions just on the specific http methods.

        params: permissions_per_method - must be a dict with the http methods
        and the permissions classes.
        Ex: { 'GET': isAuthenticated }
    """
    permissions_per_method: dict[str, type] = {}

    def get_permissions(self, *args, **kwargs):
        for method, permission in self.permissions_per_method.items():
            if self.request.method == method.upper():
                return [permission()]
            return [p() for p in self.permission_classes]
