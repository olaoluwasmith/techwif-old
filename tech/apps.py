from django.apps import AppConfig


class TechConfig(AppConfig):
    name = 'tech'

    def ready(self):
        import tech.signals