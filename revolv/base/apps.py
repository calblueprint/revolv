from django.apps import AppConfig


class RevolvBaseConfig(AppConfig):
    name = 'revolv.base'
    verbose_name = "Revolv Base User"

    def ready(self):
        import revolv.base.signals
        revolv.base.signals  # quiet the pep8 flaker
