from django.apps import AppConfig


class RevolvPaymentsConfig(AppConfig):
    name = 'revolv.payments'
    verbose_name = 'Revolv Payments'

    def ready(self):
        import signals
        signals  # silence pep8
