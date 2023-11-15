from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .. users.mocks import make_superuser


class APITestCaseWithLogin(APITestCase):
    def make_login(self) -> tuple[User, str]:
        # create a user
        user = make_superuser()

        response = self.client.post(
            '/api/token/',
            {
                'username': 'user',
                'password': '123456'
            }
        )

        token = response.data.get('access')  # type: ignore

        return user, token
