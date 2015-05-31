from exceptions import NotImplementedError
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from revolv.base.models import RevolvUserProfile


class SeedSpec(object):
    """
    A seed spec is an object which specifies a chunk of data that will be seeded into the
    database when the seed command is run. This is an abstract class: children of it, for
    example RevolvUserProfileSeedSpec or ProjectSeedSpec, must implement a few methods:

    seed(): seeds the data into the database. This function may be indempotent (that is,
        it may leave the database in the same state after being run the first time and
        the second time), but the actual indempotence is up to the specific subclass of
        SeedSpec.

    clear(): clears the data that was seeded. If there was no data seeded, this function
        should do nothing.
    """

    def seed(self):
        raise NotImplementedError("Abstract SeedSpec class tried to call seed()")

    def clear(self):
        raise NotImplementedError("Abstract SeedSpec class tried to call clear()")


class RevolvUserProfileSeedSpec(SeedSpec):
    """
    The database seed specification for revolv.base.models.RevolvUserProfile.

    Creates three users: one donor, one ambassador, and one administrator. Logins are
    donor/password, ambassador/password, administrator/password respectively.
    """
    usernames_to_clear = ["donor", "ambassador", "administrator"]

    def seed(self):
        RevolvUserProfile.objects.create_user(
            username="donor",
            email="donor@re-volv.org",
            first_name="Joe",
            last_name="Donor",
            password="password"
        )
        RevolvUserProfile.objects.create_user_as_ambassador(
            username="ambassador",
            email="ambassador@re-volv.org",
            first_name="Joe",
            last_name="Ambassador",
            password="password"
        )
        RevolvUserProfile.objects.create_user_as_admin(
            username="administrator",
            email="administrator@re-volv.org",
            first_name="Joe",
            last_name="Admin",
            password="password"
        )

    def clear(self):
        for username in self.usernames_to_clear:
            try:
                user = User.objects.get(username=username)
                RevolvUserProfile.objects.get(user=user).delete()
                user.delete()
            except User.DoesNotExist as e:
                print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


SPECS_TO_RUN = [
    RevolvUserProfileSeedSpec()
]


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--clear',
                    action='store_true',
                    dest='clear',
                    default=False,
                    help='Clear the seeded data instead of seeding it.'),
    )

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
        if options["clear"]:
            verb = "Clearing"
        else:
            verb = "Seeding"

        print "[Seed:Info] %s objects from %i seed spec(s)..." % (verb, len(SPECS_TO_RUN))
        for spec in SPECS_TO_RUN:
            if options["clear"]:
                spec.clear()
            else:
                spec.seed()
        print "[Seed:Info] Done!"
