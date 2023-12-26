from django.http import Http404
from rest_framework.request import Request
import os

TOKEN_ACCESS = os.environ.get('TOKEN_ACCESS', '')


def token_verify(func):
    """
        Checks if the client has an authorized token.
        Get the token from the url.
        If the token is invalid, an Http404 is raised
    """
    def wrapp(request: Request, *args, **kwargs):
        token = request.GET.get('token')

        if token != TOKEN_ACCESS:
            raise Http404()
        return func(request, *args, **kwargs)

    return wrapp
