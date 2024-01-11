from django.urls import reverse, resolve
from django.utils.text import slugify
from work import views
from utils.mocks.auth import APITestCaseWithLogin
from utils.mocks.work import make_work, make_image_work
from parameterized import parameterized  # type: ignore
from rest_framework_api_key.models import APIKey

title_test = 'development of a robot for instagram'
slug_test = slugify(title_test)


class WorkDetailsAPIV1Tests(APITestCaseWithLogin):
    reverse_url = 'works:work'
    url = reverse(reverse_url, args=('work-title',))

    def setUp(self, *args, **kwargs) -> None:
        _, self.key = APIKey.objects.create_key(name='my-app')
        return super().setUp(*args, **kwargs)

    def test_work_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/work/api/work-title/',
        )

    def test_work_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkCreateDetailAPIV1View,
        )

    def test_work_get_request_returns_status_code_401(self) -> None:  # noqa: E501
        response = self.client.get(self.url,)

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_work_get_request_returns_status_code_404_if_not_work(self) -> None:  # noqa: E501
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Api-Key {self.key}',
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_work_get_request_returns_status_code_200_if_work(self) -> None:
        # create an work
        make_work()

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Api-Key {self.key}',
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    @parameterized.expand([
        'id',
        'title',
        'description',
        'link',
        'images',
        'is_published',
        'show_in_home',
        title_test,
        slug_test,
        'this is my description',
        'https://my-robot.com',
        'True',
        'False'
    ])
    def test_work_get_request_returns_correct_data(self, text: str) -> None:
        # set the url
        self.url = reverse(self.reverse_url, args=(slug_test,))

        # create an work
        work = make_work(
            title=title_test,
            slug=slug_test,
            description='this is my description',
            link='https://my-robot.com',
        )

        # create 3 images for the work
        make_image_work(work_instance=work, num_of_imgs=3)

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Api-Key {self.key}',
        )

        # checks the response data
        self.assertIn(
            text,
            str(response.data),
        )

        # checks if the work has 3 images
        self.assertEqual(
            len(response.data.get('images')),  # type: ignore
            3,
        )

    def test_work_get_request_must_returns_only_your_images(self) -> None:
        # set the url
        self.url = reverse(self.reverse_url, args=(slug_test,))

        # create an work
        work = make_work(title='this is the title', slug=slug_test)

        # create 3 images for the work
        make_image_work(work_instance=work, num_of_imgs=3)

        # create another work and 2 images
        another_work = make_work(slug='another-work')
        make_image_work(work_instance=another_work, num_of_imgs=2)

        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Api-Key {self.key}',
        )

        # checks if the work has 3 images
        self.assertEqual(
            len(response.data.get('images')),  # type: ignore
            3,
        )
