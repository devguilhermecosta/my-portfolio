from utils.mocks.auth import APITestCaseWithLogin
from django.urls import reverse, resolve
from django.test import override_settings
from work import views
from utils.mocks.work import make_image_work, make_work
from utils.mocks.images import make_simple_image
from parameterized import parameterized  # type: ignore
import contextlib
import shutil


TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ImageWorksApiV1Tests(APITestCaseWithLogin):
    url = reverse('works:images-work', args=(1,))

    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def test_image_works_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/api/work/1/images/',
        )

    def test_image_works_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,  # type: ignore
            views.WorkImagesAPIView,
        )

    def test_image_works_get_request_returns_status_code_200_if_images(self) -> None:  # noqa: E501

        make_image_work()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_image_works_get_request_returns_status_code_404_if_images_not_found(self) -> None:  # noqa: E501
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    @parameterized.expand([
        'id',
        'url',
    ])
    def test_images_work_returns_correct_data_when_get_request(self,
                                                               content: str,
                                                               ) -> None:
        # make 3 images objects
        make_image_work(num_of_imgs=3)

        response = self.client.get(self.url)

        # checks if the work has 3 images objects
        self.assertEqual(
            len(response.data),  # type: ignore
            3,
        )

        # check images data
        self.assertIn(
            content,
            str(response.data),
        )

    def test_images_work_post_request_is_not_allowed_without_a_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            401,
        )

    @parameterized.expand([
        ('work_id', 'Campo obrigatório'),
        ('url', 'Envie somente imagens'),
    ])
    def test_images_work_post_request_returns_error_messages_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        data = {
            field: '',
        }

        response = self.client.post(
            self.url,
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertIn(
            msg,
            str(response.data[field][0])  # type: ignore
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_images_work_post_request_returns_status_code_201_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make a work object with id = 1
        make_work()

        # make a simple image
        image = make_simple_image()

        response = self.client.post(
            self.url,
            {
                'work_id': 1,
                'url': image,
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_images_work_patch_request_returns_status_code_401_if_not_a_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.patch(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_images_work_patch_request_returns_status_code_404_if_not_a_valid_image_object(self) -> None:  # noqa: E501
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
        ('work_id', 'Campo obrigatório'),
    ])
    def test_images_work_patch_request_returns_error_message_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make a image object
        make_image_work()

        data = {
            field: '',
        }

        response = self.client.patch(
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

    def test_images_work_patch_request_returns_status_code_204_if_the_object_is_updated(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make a image object
        make_image_work()

        # created another simple image
        another_image = make_simple_image()

        response = self.client.patch(
            self.url,
            data={
                'url': another_image,
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )

    def test_images_work_delete_request_returns_status_code_401_if_not_a_valid_jwt_token(self) -> None:  # noqa: E501
        response = self.client.delete(
            self.url,
        )
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_images_work_delete_request_returns_status_code_404_if_image_not_found(self) -> None:  # noqa: E501
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

    def test_images_work_delete_request_returns_status_code_204_if_the_image_is_deleted(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make an image object
        make_image_work()

        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )
