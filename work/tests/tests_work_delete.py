from utils.mocks.auth import APITestCaseWithLogin
from django.urls import reverse, resolve
from work import views
from utils.mocks.work import make_work
from rest_framework_api_key.models import APIKey


class WorkDeleteAPIV1Tests(APITestCaseWithLogin):
    url = reverse('works:work', args=('work-title',))

    def test_work_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/work-title/',
        )

    def test_work_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkCreateDetailAPIV1View,
        )

    def test_work_delete_returns_status_code_401_if_not_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.delete(self.url)

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_work_delete_returns_status_code_404_if_no_work(self) -> None:
        # make login
        _, token = self.make_login()

        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_work_delete_removes_the_work_from_db_and_returns_status_code_204(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # create an work
        make_work()

        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )

        # checks if the work exists
        _, key = APIKey.objects.create_key(name='my-app')
        get_work = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=F'Api-Key {key}',
        )

        self.assertEqual(
            get_work.status_code,
            404,
        )
