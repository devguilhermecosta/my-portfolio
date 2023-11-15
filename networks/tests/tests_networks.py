from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .. import views
from .. models import Networks
from parameterized import parameterized  # type: ignore


def make_networks() -> Networks:
    """
        make a new instance of Networks
    """
    obj = Networks.objects.create(
        instagram="https://www.instagram.com",
        linkedin="https://www.linkedin.com",
        github="https://www.github.com",
        whatsapp="https://www.whatsapp.com",
        phone="46999083251",
        email="guilherme.partic@gmail.com",
        )
    obj.save()
    return obj


def make_superuser() -> User:
    user = User.objects.create_superuser(
        username='user',
        password='123456',
        email='email@email.com',
        )
    user.save()
    return user


class NetowrksAPITests(APITestCase):
    url = reverse('networks:networks')

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

    def test_networks_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/networks/api/v1/',
        )

    def test_networks_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,  # type: ignore
            views.NetworksApiV1View,
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

    def test_networks_post_request_returns_status_code_201_with_a_valid_jwt_token_and_data(self) -> None:  # noqa: E501
        # make login
        _, token = self.make_login()

        # make a post request
        response = self.client.post(
            self.url,
            {
                "instagram": "https://www.instagram.com",
                "linkedin": "https://www.linkedin.com",
                "github": "https://www.github.com",
                "whatsapp": "https://www.whatsapp.com",
                "phone": "46999083251",
                "email": "guilherme.partic@gmail.com"
            },
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        self.assertEqual(
            response.status_code,
            201,
        )

# comando para rodar os testes: ptw -c -- -k 'NomeDaClasse' -rP -v
