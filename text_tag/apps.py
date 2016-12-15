from django.apps import AppConfig


class TextTagConfig(AppConfig):
    name = 'text_tag'

    def ready(self):
        from text_tag import registry
        registry.autodiscover()