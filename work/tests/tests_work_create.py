from utils.mocks.auth import APITestCaseWithLogin
from django.urls import reverse, resolve
from work import views
from parameterized import parameterized  # type: ignore
from utils.mocks.images import make_simple_image
from utils.mocks.work import make_work


class WorkCreateAPIV1Tests(APITestCaseWithLogin):
    url = reverse('works:work-create')

    def test_work_post_request_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/create/',
        )

    def test_work_post_request_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,  # type: ignore
            views.WorkCreateDetailAPIV1View,
        )

    def test_work_post_request_returns_status_code_401_without_a_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            401,
        )

    @parameterized.expand([
        ('title', 'Campo obrigatório'),
        ('description', 'Campo obrigatório'),
        ('cover', 'Envie somente imagens'),
    ])
    def test_work_post_request_returns_error_messages_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        _, token = self.make_login()

        # work data
        data = {
            field: '',
        }

        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
            )

        self.assertIn(
            msg,
            str(response.data[field]),  # type: ignore
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_work_post_request_returns_error_message_if_the_title_and_slug_exists(self) -> None:  # noqa: E501
        # work data
        data = {
            'title': 'work title',
            'slug': 'work-title',
            'description': 'work description',
        }

        # make a work
        make_work(**data)

        # make login
        _, token = self.make_login()

        # tries create a new obj with same data
        response = self.client.post(
            self.url,
            {
                **data,
                'cover': make_simple_image(),
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
            )

        response_data = response.data

        self.assertIn(
            'work com este slug já existe',
            str(response_data['slug']),  # type: ignore
        )

        self.assertIn(
            'work com este title já existe',
            str(response_data['title']),  # type: ignore
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_work_post_request_returns_status_code_201_if_the_obj_is_created(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # tries create a new obj with as little information as possible​
        response = self.client.post(
            self.url,
            {
                'title': 'work title',
                'description': 'work description',
                'cover': make_simple_image(),
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
            )

        self.assertEqual(
            response.status_code,
            201,
        )
