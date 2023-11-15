from django.contrib.auth.models import User


def make_superuser() -> User:
    user = User.objects.create_superuser(
        username='user',
        password='123456',
        email='email@email.com',
        )
    user.save()
    return user
