import datetime
from exceptions import NotImplementedError
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from revolv.base.models import RevolvUserProfile
from revolv.project.models import Project


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


class ProjectSeedSpec(SeedSpec):
    """
    Database seed specification for revolv.project.models.Project

    Creates 4 projects with various settings: Community Dairy, Community Dance Studio,
    Educathing, and Fire Emblem.

    TODO: Make this spec create projects that mirror the projects that RE-volv has already
    completed.
    """
    studio = {
        "funding_goal": 12000.0,
        "title": "Power Community Dance Studio",
        "tagline": "Dance forever, dance until dawn.",
        "video_url": "https://www.youtube.com/watch?v=fzShzO2pk-E",
        "org_name": "The Community Dance Studio",
        "impact_power": 10.0,
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "location": "2415 Bowditch St, Berkeley, CA 94704, United States",
        "location_latitude": 37.8670289,
        "location_longitude": -122.2561597,
        "actual_energy": 0.0,
        "end_date": datetime.date(2050, 10, 8),
        "cover_photo": "covers/box.jpg",
        "org_start_date": datetime.date(1995, 10, 9),
        "mission_statement": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "org_about": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).\r\n",
        "internal_rate_return": 7.8
    }
    projects = [studio]

    def seed(self):
        ambassador = RevolvUserProfile.objects.get(user__username="ambassador")
        Project.factories.active.create(ambassador=ambassador, **self.studio)
        # Project.factories.completed.create(ambassador=ambassador, **self.dairy)
        # Project.factories.proposed.create(ambassador=ambassador, **self.educathing)
        # Project.factories.drafted.create(ambassador=ambassador, **self.emblem)

    def clear(self):
        for project in self.projects:
            try:
                Project.objects.get(tagline=project["tagline"]).delete()
            except Project.DoesNotExist as e:
                print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


SPECS_TO_RUN = [
    RevolvUserProfileSeedSpec(),
    ProjectSeedSpec()
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
