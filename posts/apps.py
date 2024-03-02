from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'posts'
