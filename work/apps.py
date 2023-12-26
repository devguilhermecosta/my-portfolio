from django.apps import AppConfig


class WorkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'work'

    def ready(self, *args, **kwargs) -> None:
        import work.signals  # noqa: F401
        return super().ready(*args, **kwargs)
