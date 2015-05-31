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
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "The Community Dance Studio",
        "impact_power": 10.0,
        "actual_energy": 0.0,
        "location": "2415 Bowditch St, Berkeley, CA 94704, United States",
        "location_latitude": 37.8670289,
        "location_longitude": -122.2561597,
        "end_date": datetime.date(2050, 10, 8),
        "cover_photo": "covers/box.jpg",
        "org_start_date": datetime.date(1995, 10, 9),
        "mission_statement": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "org_about": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).\r\n",
        "internal_rate_return": 7.8
    }
    dairy = {
        "funding_goal": 14000.00,
        "title": "Power for Comoonity Dairy",
        "tagline": "Some say that milk is power.",
        "video_url": "https://www.youtube.com/watch?v=JtA8gqWA6PE",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "Comoonity Dairy",
        "impact_power": 12.0,
        "actual_energy": 0.0,
        "location": "1238 5th Street, Berkeley, CA, United States",
        "location_latitude": 37.87968940000000,
        "location_longitude": -122.30289330000000,
        "end_date": datetime.date(2175, 1, 1),
        "cover_photo": "covers/Dairy-Products-vitamin-D-foods.jpg",
        "org_start_date": datetime.date(1997, 10, 9),
        "mission_statement": "With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "description": "With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "org_about": "The idea that companies should prioritize phones and tablets over old-school PCs isn't new, and companies like Google claim to have been doing it for years. But what they're finally realizing is that mobile-first means more than just making a finely polished app for touch screens. User behavior isn't the same on phones as it is on PCs, which means the app itself must be fundamentally different.\r\n\r\nMicrosoft's Sway, for instance, throws out most of the robust tools that PowerPoint offers, and instead focuses on letting people throw things together quickly, even on a smartphone. It's sort of like using templates in PowerPoint, except that each slide can adapt to the amount of photos and text you put in it, and will format itself automatically for any screen size.",
        "internal_rate_return": 7.5,
    }
    educathing = {
        "funding_goal": 22000.00,
        "title": "Some Education Thing",
        "tagline": "Our children need to learn.",
        "video_url": "https://www.youtube.com/watch?v=slbco4zHmt8",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "Educathing",
        "actual_energy": 0.0,
        "impact_power": 18.0,
        "location": "School, Oakland, CA, United States",
        "location_latitude": "37.79515640000000",
        "location_longitude": "-122.21575089999999",
        "end_date": datetime.date(2200, 01, 01),
        "cover_photo": "covers/education.jpg",
        "org_start_date": datetime.date(1980, 01, 01),
        "mission_statement": "The Internship, which opens on June 7, finds Vince Vaughn and Owen Wilson playing middle-aged watch salesmen who are dinosaurs when it comes to technology. The guys become Google interns--this is a comedy, so just suspend your disbelief--to learn all they can about the digital world. The aspiring tech experts hope to get jobs at Google when all is said and done, but they must beat out brilliant geeks for the coveted positions. Leaving aside the creative merits of the film (just about every reviewer has called The Internship an unabashed, two-hour ad for Google), it does explore a hypothetically interesting topic--what it\u2019s like to make the grade at the competitive corporate promised land of the Internet age.\r\n",
        "description": "The Internship, which opens on June 7, finds Vince Vaughn and Owen Wilson playing middle-aged watch salesmen who are dinosaurs when it comes to technology. The guys become Google interns--this is a comedy, so just suspend your disbelief--to learn all they can about the digital world. The aspiring tech experts hope to get jobs at Google when all is said and done, but they must beat out brilliant geeks for the coveted positions. Leaving aside the creative merits of the film (just about every reviewer has called The Internship an unabashed, two-hour ad for Google), it does explore a hypothetically interesting topic--what it\u2019s like to make the grade at the competitive corporate promised land of the Internet age.\r\n",
        "org_about": "The environment for interns at Google is healthier than it might be portrayed in the movie Ewing says with a laugh, noting, \u201cOne of the biggest differences between the movie and a real internship at Google is that interns are not competing against each other, not for jobs or anything else. We would never pit them against each other.\u201d\r\n\r\nIn addition to working in what Ewing describes as a supportive and collaborative environment, Google interns enjoy competitive pay and perks, and interning can indeed be a path to a full-time job.",
        "internal_rate_return": 7.2,
    }
    emblem = {
        "funding_goal": 24000.00,
        "title": "Roy's our Boy!",
        "tagline": "The force is strong with this boy.",
        "video_url": "https://www.youtube.com/watch?v=I7WqXwb4GQg",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "Fire Emblem",
        "actual_energy": 0.0,
        "impact_power": 18.0,
        "location": "140 New Montgomery, San Francisco, CA, United States",
        "location_latitude": "37.79515640000000",
        "location_longitude": "-122.21575089999999",
        "end_date": datetime.date(2200, 01, 01),
        "cover_photo": "covers/education.jpg",
        "org_start_date": datetime.date(1980, 01, 01),
        "mission_statement": "Fire Emblem, the best game ever.",
        "description": "Fire Emblem, the best game ever.",
        "org_about": "Embark with our heroes on a quest to save the world!",
        "internal_rate_return": 7.0,
    }
    projects_to_clear = [studio, dairy, educathing, emblem]

    def seed(self):
        ambassador = RevolvUserProfile.objects.get(user__username="ambassador")
        Project.factories.active.create(ambassador=ambassador, **self.studio)
        Project.factories.completed.create(ambassador=ambassador, **self.dairy)
        Project.factories.proposed.create(ambassador=ambassador, **self.educathing)
        Project.factories.drafted.create(ambassador=ambassador, **self.emblem)

    def clear(self):
        for project in self.projects_to_clear:
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
