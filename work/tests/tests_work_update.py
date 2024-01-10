from utils.mocks.auth import APITestCaseWithLogin
from django.urls import reverse, resolve
from work import views
from parameterized import parameterized  # type: ignore
from utils.mocks.work import make_work
from rest_framework_api_key.models import APIKey


class WorkUpdateAPIV1Tests(APITestCaseWithLogin):
    url = reverse('works:work', args=('work-title',))

    def test_work_update_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/work-title/',
        )

    def test_work_update_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkCreateDetailAPIV1View,
        )

    def test_work_update_returns_status_code_401_if_not_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.patch(self.url)

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_work_update_returns_status_code_404_if_no_work(self) -> None:
        # make login
        _, token = self.make_login()

        response = self.client.patch(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    @parameterized.expand([
        ('title', 'Campo obrigatório'),
        ('description', 'Campo obrigatório'),
        ('cover', 'Envie somente imagens'),
    ])
    def test_work_returns_status_code_400_if_required_field_is_blank(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make work
        make_work()

        # work data
        data = {
            field: '',
        }

        response = self.client.patch(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.assertIn(
            msg,
            str(response.data[field])  # type: ignore
        )

    def test_work_update_returns_status_code_204(self) -> None:
        # make login
        _, token = self.make_login()

        # make work
        make_work()

        # work data
        data = {
            'title': 'another title',
        }

        response = self.client.patch(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )

    def test_work_update_changes_the_work_fields(self) -> None:
        # make login
        _, token = self.make_login()

        # make work
        make_work()

        # work data
        another_title = 'another title'
        data = {
            'title': another_title,
        }

        self.client.patch(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        # get the work
        _, key = APIKey.objects.create_key(name='my-app')
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Api-Key {key}',
        )

        work_data = response.data['title']  # type: ignore

        self.assertEqual(
            work_data,
            another_title,
        )
