from django.apps import AppConfig


class BusinessConfig(AppConfig):
    name = 'business'
    verbose_name = "Business Class"

    def ready(self):
        import signals
