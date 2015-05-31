from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        This handle function is run when the command "python manage.py seed" is run.

        This command seeds the development database. That is, it creates a bunch of dummy
        database entries that are useful for development, like a user account of each type,
        a few projects with varying levels of donation, etc.

        This function is intended to replace loading data in with fixtures, which can
        sometimes cause problems, especially if the models they're loading have signals
        associated with them. This function fully expects signals to be enabled, and will
        create objects knowing that signals will be run on the creation of some of them.
        """
        print "The seed command was run!"
        pass  # right now do nothing
