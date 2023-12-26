from django.urls import reverse, resolve
from work import views
from utils.mocks.auth import APITestCaseWithLogin
from utils.mocks.work import make_work_in_batch
from parameterized import parameterized  # type: ignore
from unittest.mock import patch
import re


class WorkListAPIV1Tests(APITestCaseWithLogin):
    url = reverse('works:work-list')

    def test_work_list_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/list/',
        )

    def test_work_list_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkListAPIV1View,
        )

    def test_work_list_get_request_returns_status_code_200(self) -> None:
        with patch('utils.auth.decorators.token_verify.TOKEN_ACCESS', new='abc'):  # noqa: E501
            response = self.client.get(self.url, {'token': 'abc'})

            self.assertEqual(
                response.status_code,
                200,
            )

    def test_work_list_get_request_returns_a_query_set_of_work_objects(self) -> None:  # noqa: E501
        # creates 4 works
        make_work_in_batch(
            num_of_works=4,
            with_images=True,
            num_of_images_per_obj=2,
        )

        with patch('utils.auth.decorators.token_verify.TOKEN_ACCESS', new='abc'):  # noqa: E501
            response = self.client.get(self.url, {'token': 'abc'})

            self.assertEqual(
                len(response.data),  # type: ignore
                4,
            )

    @parameterized.expand([
        'id',
        'title',
        'slug',
        'description',
        'link',
        'cover',
        'created_at',
        'images',
        '1',                            # id
        'work title - num 0',           # title
        'work-title-0',                 # slug
        'this is the the description',  # description
    ])
    def test_work_list_get_request_returns_correct_content(self, text: str) -> None:  # noqa: E501
        # creates 2 works
        make_work_in_batch(
            num_of_works=2,
            with_images=True,
            num_of_images_per_obj=1,
        )

        with patch('utils.auth.decorators.token_verify.TOKEN_ACCESS', new='abc'):  # noqa: E501
            response = self.client.get(self.url, {'token': 'abc'})

            self.assertIn(
                text,
                str(response.data),
            )

            # created_at
            self.assertTrue(
                re.match(
                    r'^\d{4}(-\d{2}){2}',
                    str(response.data[0]['created_at']),  # type: ignore
                    )
            )
