from django.apps import AppConfig


class RevolvProjectConfig(AppConfig):
    name = 'revolv.project'
    verbose_name = "Revolv Project"

    def ready(self):
        import revolv.project.signals
        #signals  # quiet the pep8 flaker