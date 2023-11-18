from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import override_settings
from .. users.mocks import make_superuser
import contextlib
import shutil


TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class APITestCaseWithLogin(APITestCase):
    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

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
