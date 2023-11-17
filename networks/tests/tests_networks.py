from django.urls import reverse, resolve
from .. import views
from .. models import Networks
from parameterized import parameterized  # type: ignore
from utils.mocks.networks import make_networks
from utils.mocks.auth import APITestCaseWithLogin


class NetowrksAPITests(APITestCaseWithLogin):
    url = reverse('networks:networks')

    def setUp(self) -> None:
        self.api_data = {
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "whatsapp": "https://www.whatsapp.com",
            "phone": "46999083251",
            "email": "guilherme.partic@gmail.com"
            }

        return super().setUp()

    def test_networks_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/api/networks/api/v1/',
        )

    def test_networks_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,  # type: ignore
            views.NetworksApiV1View,
        )

    def test_networks_get_queryset_moethod_returns_the_first_obj(self) -> None:
        # make a network obj
        network = make_networks()

        view = views.NetworksApiV1View()

        self.assertEqual(
            view.get_queryset(),
            network,
        )

    def test_networks_returns_status_code_404_when_get_request_and_if_no_networks(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_networks_returns_status_code_200_when_get_request_and_exists_an_networks_object(self) -> None:  # noqa:E 501
        make_networks()
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_networks_post_request_returns_status_code_401_without_a_jwt_token(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            401,
        )

    @parameterized.expand([
        ('linkedin', 'Campo obrigatório'),
        ('instagram', 'Campo obrigatório'),
        ('github', 'Campo obrigatório'),
        ('whatsapp', 'Campo obrigatório'),
        ('phone', 'Campo obrigatório'),
        ('email', 'Campo obrigatório'),
    ])
    def test_networks_post_request_returns_error_message_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # networks data
        data = {
            field: '',
        }

        # make a post request
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        self.assertIn(
            msg,
            str(response.data[field][0]),  # type: ignore
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_networks_post_request_returns_status_code_201_with_a_valid_jwt_token_and_data(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make a post request
        response = self.client.post(
            self.url,
            self.api_data,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        self.assertEqual(
            response.status_code,
            201,
        )

    def test_networks_post_request_returns_status_code_200_if_the_networks_obj_exists(self) -> None:  # noqa: E501
        """
            There must be only one networks object.
            When the user tries to create a second or third object,
            the first object will be returned, and nothind else.
        """

        # create a first object
        make_networks()

        # get a token
        _, token = self.make_login()

        # tries criate a second object
        # make a post request
        response = self.client.post(
            self.url,
            self.api_data,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            len(Networks.objects.all()),
            1,
        )

    def test_networks_patch_request_returns_status_code_404_if_no_networks(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make patch request
        response = self.client.patch(
            self.url,
            data={
                'github': 'https://www.github.com',
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_networks_patch_request_returns_status_code_401_if_no_jwt_token(self) -> None:  # noqa: E501
        # make patch request
        response = self.client.patch(
            self.url,
            data={
                'github': 'https://www.github.com',
            },
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_networks_patch_request_returns_status_code_400_if_any_field_is_empty(self) -> None:  # noqa: E501
        # make a networks obj
        make_networks()

        # make login
        _, token = self.make_login()

        # make patch request
        response = self.client.patch(
            self.url,
            data={
                'github': '',
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertEqual(
            str(response.data.get('github')[0]),  # type: ignore
            'Campo obrigatório',
        )

    def test_networks_patch_request_returns_status_code_204_if_the_modified_field_is_ok(self) -> None:  # noqa: E501
        # make a networks obj
        make_networks()

        # make login
        _, token = self.make_login()

        # data attribute
        data_attr = 'https://field_link.com'

        # make patch request
        response = self.client.patch(
            self.url,
            data={
                'github': data_attr,
            },
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(
            response.status_code,
            204,
        )
        self.assertEqual(
            Networks.objects.first().github,  # type: ignore
            data_attr,
        )
