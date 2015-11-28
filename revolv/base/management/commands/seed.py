import datetime
from exceptions import NotImplementedError
from optparse import make_option

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import Payment, ProjectMontlyRepaymentConfig
from revolv.project.models import Project
from revolv.revolv_cms.models import RevolvCustomPage, RevolvLinkPage
from wagtail.wagtailcore.models import Page, Site
from wagtailsettings.registry import registry as settings_registry


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

    def seed(self, quiet=False):
        raise NotImplementedError("Abstract SeedSpec class tried to call seed()")

    def clear(self, quiet=False):
        raise NotImplementedError("Abstract SeedSpec class tried to call clear()")


class RevolvUserProfileSeedSpec(SeedSpec):
    """
    The database seed specification for revolv.base.models.RevolvUserProfile.

    Creates 7 users: 5 donor, one ambassador, and one administrator. Logins are
    donorX/password, ambassador/password, administrator/password respectively.
    """
    usernames_to_clear = []

    def seed(self, quiet=False):
        RevolvUserProfile.objects.create_user(
            username="donor",
            email="donor@re-volv.org",
            first_name="Joe",
            last_name="Donor",
            password="password"
        )
        RevolvUserProfile.objects.create_user(
            username="donor2",
            email="donor2@re-volv.org",
            first_name="Joe2",
            last_name="Donor2",
            password="password"
        )
        RevolvUserProfile.objects.create_user(
            username="donor3",
            email="donor3@re-volv.org",
            first_name="Joe3",
            last_name="Donor3",
            password="password"
        )
        RevolvUserProfile.objects.create_user(
            username="donor4",
            email="donor4@re-volv.org",
            first_name="Joe4",
            last_name="Donor4",
            password="password"
        )
        RevolvUserProfile.objects.create_user(
            username="donor5",
            email="donor5@re-volv.org",
            first_name="Joe5",
            last_name="Donor5",
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

    def clear(self, quiet=False):
        if self.usernames_to_clear:
            for username in self.usernames_to_clear:
                try:
                    user = User.objects.get(username=username)
                    RevolvUserProfile.objects.get(user=user).delete()
                    user.delete()
                except User.DoesNotExist as e:
                    if not quiet:
                        print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))
        else:
            RevolvUserProfile.objects.all().delete()
            User.objects.all().delete()


class ProjectSeedSpec(SeedSpec):
    """
    Database seed specification for revolv.project.models.Project

    Creates 3 completed projects, 3 active projects, and 1 draft

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
        "start_date": datetime.date(2014, 1, 1),
        # community dance studio is in progress, two months til deadline
        "end_date": datetime.date.today() + datetime.timedelta(weeks=8),
        "cover_photo": "covers/box.jpg",
        "org_start_date": datetime.date(1995, 10, 9),
        "mission_statement": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "org_about": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).\r\n",
        "internal_rate_return": 7.8
    }

    studio2 = {
        "funding_goal": 14000.0,
        "title": "Power Community Dance Studio 2",
        "tagline": "Dance forever, dance until dawn. 2",
        "video_url": "https://www.youtube.com/watch?v=fzShzO2pk-E",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "The Community Dance Studio 2",
        "impact_power": 11.0,
        "actual_energy": 0.0,
        "location": "2415 Bowditch St, Berkeley, CA 94704, United States",
        "location_latitude": 37.8670289,
        "location_longitude": -122.2561597,
        "start_date": datetime.date(2014, 1, 1),
        # community dance studio is in progress, two months til deadline
        "end_date": datetime.date.today() + datetime.timedelta(weeks=7),
        "cover_photo": "covers/box.jpg",
        "org_start_date": datetime.date(1995, 10, 9),
        "mission_statement": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\r\n",
        "org_about": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).\r\n",
        "internal_rate_return": 7.8
    }

    studio3 = {
        "funding_goal": 10000.0,
        "title": "Power Community Dance Studio 3",
        "tagline": "Dance forever, dance until dawn. 3",
        "video_url": "https://www.youtube.com/watch?v=fzShzO2pk-E",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "The Community Dance Studio 3",
        "impact_power": 11.0,
        "actual_energy": 0.0,
        "location": "2415 Bowditch St, Berkeley, CA 94704, United States",
        "location_latitude": 37.8670289,
        "location_longitude": -122.2561597,
        "start_date": datetime.date(2014, 1, 1),
        # community dance studio is in progress, two months til deadline
        "end_date": datetime.date.today() + datetime.timedelta(weeks=7),
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
        "start_date": datetime.date(2014, 1, 1),
        "end_date": datetime.date(2015, 1, 1),  # this project is already complete
        "cover_photo": "covers/Dairy-Products-vitamin-D-foods.jpg",
        "org_start_date": datetime.date(1997, 10, 9),
        "mission_statement": "With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "description": "With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "org_about": "The idea that companies should prioritize phones and tablets over old-school PCs isn't new, and companies like Google claim to have been doing it for years. But what they're finally realizing is that mobile-first means more than just making a finely polished app for touch screens. User behavior isn't the same on phones as it is on PCs, which means the app itself must be fundamentally different.\r\n\r\nMicrosoft's Sway, for instance, throws out most of the robust tools that PowerPoint offers, and instead focuses on letting people throw things together quickly, even on a smartphone. It's sort of like using templates in PowerPoint, except that each slide can adapt to the amount of photos and text you put in it, and will format itself automatically for any screen size.",
        "internal_rate_return": 7.5,
    }
    dairy2 = {
        "funding_goal": 20000.00,
        "title": "Music rulezz",
        "tagline": "Some say that music is power.",
        "video_url": "https://www.youtube.com/watch?v=JtA8gqWA6PE",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "Indie",
        "impact_power": 15.0,
        "actual_energy": 0.0,
        "location": "1238 10th Street, Berkeley, CA, United States",
        "location_latitude": 37.88968940000000,
        "location_longitude": -122.30289330000000,
        "start_date": datetime.date(2014, 1, 1),
        "end_date": datetime.date(2015, 1, 1),  # this project is already complete
        "cover_photo": "covers/Dairy-Products-vitamin-D-foods.jpg",
        "org_start_date": datetime.date(1990, 10, 9),
        "mission_statement": "Copy from Diary: With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "description": "Copy from Diary: With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "org_about": "Copy from Diary: The idea that companies should prioritize phones and tablets over old-school PCs isn't new, and companies like Google claim to have been doing it for years. But what they're finally realizing is that mobile-first means more than just making a finely polished app for touch screens. User behavior isn't the same on phones as it is on PCs, which means the app itself must be fundamentally different.\r\n\r\nMicrosoft's Sway, for instance, throws out most of the robust tools that PowerPoint offers, and instead focuses on letting people throw things together quickly, even on a smartphone. It's sort of like using templates in PowerPoint, except that each slide can adapt to the amount of photos and text you put in it, and will format itself automatically for any screen size.",
        "internal_rate_return": 7.5,
    }
    dairy3 = {
        "funding_goal": 10000.00,
        "title": "Karate kid",
        "tagline": "I'll kick you.",
        "video_url": "https://www.youtube.com/watch?v=JtA8gqWA6PE",
        "solar_url": "http://home.solarlog-web.net/1445.html",
        "org_name": "Karate Inc",
        "impact_power": 19.0,
        "actual_energy": 0.0,
        "location": "1238 11th Street, Berkeley, CA, United States",
        "location_latitude": 37.88868940000000,
        "location_longitude": -122.30289330000000,
        "start_date": datetime.date(2014, 1, 1),
        "end_date": datetime.date(2015, 1, 1),  # this project is already complete
        "cover_photo": "covers/Dairy-Products-vitamin-D-foods.jpg",
        "org_start_date": datetime.date(1970, 10, 9),
        "mission_statement": "Copy from Diary 2: With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "description": "Copy from Diary 2 : With Paper, Facebook has effectively rebooted its core News Feed product on the iPhone. Although Paper is built largely around the same photos and status updates you get from Facebook's main app, it doesn't feel like something that was merely retrofitted to the phone. It emphasizes large photos and swipe gestures, and lets you add general news sections for when you need a break from your friends. It could easily stand in for the main Facebook experience, even if it doesn't have all the same features.\r\n\r\nFacebook isn't alone. Last week, Google announced Inbox, which is built around Gmail but with a different approach to displaying and handling messages. Instead of showing every email in reverse-chronological order, Inbox intelligently sorts messages into groups like \u201cTravel\u201d and \u201cPurchases,\u201d and in a nod to Dropbox's Mailbox, lets you snooze or pin important emails for later.",
        "org_about": "Copy from Diary 2: The idea that companies should prioritize phones and tablets over old-school PCs isn't new, and companies like Google claim to have been doing it for years. But what they're finally realizing is that mobile-first means more than just making a finely polished app for touch screens. User behavior isn't the same on phones as it is on PCs, which means the app itself must be fundamentally different.\r\n\r\nMicrosoft's Sway, for instance, throws out most of the robust tools that PowerPoint offers, and instead focuses on letting people throw things together quickly, even on a smartphone. It's sort of like using templates in PowerPoint, except that each slide can adapt to the amount of photos and text you put in it, and will format itself automatically for any screen size.",
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
    projects_to_clear = [studio, studio2, studio3, dairy, dairy2, dairy3, educathing, emblem]

    def seed(self, quiet=False):
        ambassador = RevolvUserProfile.objects.get(user__username="ambassador")
        Project.factories.active.create(ambassador=ambassador, **self.studio)
        Project.factories.active.create(ambassador=ambassador, **self.studio2)
        Project.factories.active.create(ambassador=ambassador, **self.studio3)
        p_complete1 = Project.factories.completed.create(ambassador=ambassador, **self.dairy)
        p_complete2 = Project.factories.completed.create(ambassador=ambassador, **self.dairy2)
        p_complete3 = Project.factories.completed.create(ambassador=ambassador, **self.dairy3)
        Project.factories.proposed.create(ambassador=ambassador, **self.educathing)
        Project.factories.drafted.create(**self.emblem)

        ProjectMontlyRepaymentConfig.objects.create(project=p_complete1,
                                                           year=2015, repayment_type='SSF',
                                                           amount=150)
        ProjectMontlyRepaymentConfig.objects.create(project=p_complete2,
                                                           year=2015, repayment_type='SSF',
                                                           amount=200)
        ProjectMontlyRepaymentConfig.objects.create(project=p_complete3,
                                                           year=2015, repayment_type='SSF',
                                                           amount=100)
        p_complete1.paid_off()
        p_complete2.paid_off()
        p_complete3.paid_off()

    def clear(self, quiet=False):
        for project in self.projects_to_clear:
            try:
                Project.objects.get(tagline=project["tagline"]).delete()
            except Project.DoesNotExist as e:
                if not quiet:
                    print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


class PaymentSeedSpec(SeedSpec):
    """
    Database seed specification for revolv.payments.models.Payment.

    Makes 8 dummy payments. For details, see the seed() method.
    """

    def seed(self, quiet=False):
        donor = RevolvUserProfile.objects.get(user__username="donor")
        donor2 = RevolvUserProfile.objects.get(user__username="donor2")
        donor3 = RevolvUserProfile.objects.get(user__username="donor3")
        donor4 = RevolvUserProfile.objects.get(user__username="donor4")
        studio = Project.objects.get(tagline=ProjectSeedSpec.studio["tagline"])
        studio2 = Project.objects.get(tagline=ProjectSeedSpec.studio2["tagline"])
        dairy = Project.objects.get(tagline=ProjectSeedSpec.dairy["tagline"])
        dairy2 = Project.objects.get(tagline=ProjectSeedSpec.dairy2["tagline"])
        dairy3 = Project.objects.get(tagline=ProjectSeedSpec.dairy3["tagline"])

        Payment.factories.base.create(project=dairy, user=donor, entrant=donor, amount=0.3 * float(dairy.funding_goal))
        Payment.factories.base.create(project=dairy, user=donor2, entrant=donor2, amount=0.7 * float(dairy.funding_goal))

        Payment.factories.base.create(project=dairy2, user=donor2, entrant=donor2, amount=0.3 * float(dairy2.funding_goal))
        Payment.factories.base.create(project=dairy2, user=donor3, entrant=donor3, amount=0.7 * float(dairy2.funding_goal))

        Payment.factories.base.create(project=dairy3, user=donor3, entrant=donor3, amount=0.3 * float(dairy3.funding_goal))
        Payment.factories.base.create(project=dairy3, user=donor4, entrant=donor4, amount=0.7 * float(dairy3.funding_goal))

        Payment.factories.base.create(project=studio, user=donor, entrant=donor, amount=11910.0)
        Payment.factories.base.create(project=studio2, user=donor3, entrant=donor3, amount=500.0)

    def clear(self, quiet=False):
        try:
            donor = RevolvUserProfile.objects.get(user__username="donor")
            donor2 = RevolvUserProfile.objects.get(user__username="donor2")
            donor3 = RevolvUserProfile.objects.get(user__username="donor3")
            donor4 = RevolvUserProfile.objects.get(user__username="donor4")

            Payment.objects.payments(user=donor).delete()
            Payment.objects.payments(user=donor2).delete()
            Payment.objects.payments(user=donor3).delete()
            Payment.objects.payments(user=donor4).delete()
        except RevolvUserProfile.DoesNotExist as e:
            if not quiet:
                print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


class CMSPageSeedSpec(SeedSpec):
    """
    Database seed specification for Wagtail CMS pages. Creates a bunch of
    RevolvCustomPages and RevolvLinkPages that comprise the nav and footer
    menus for the RE-volv app (or at least, the pages that did when this
    spec was written). You can see the page hierarchy in the page_hierarchy,
    where one page is represented by a tuple of <type (link or page)>, <title>,
    and <data (either children or href, depending on type)>.

    At this time, there's no easy one-liner for publishing a wagtail page
    programatically, so this class contains a few helper functions to publish
    pages and also to recursively traverse page_hierarchy so as to keep this code
    as DRY as possible.
    """
    page_hierarchy = [
        ("page", "About Us", [
            ("link", "Our Mission", "/about-us/"),
            ("page", "Our Team", []),
            ("page", "Partners", []),
            ("page", "Jobs", []),
        ]),
        ("page", "What We Do", [
            ("page", "How It Works", []),
            ("page", "Projects", []),
            ("link", "Solar In Your Community", "/what-we-do/"),
        ]),
        ("page", "Get Involved", [
            ("link", "Donate to the Solar Seed Fund", "/get-involved/"),
            ("page", "Solar Ambassador Program", []),
            ("page", "Support Us", []),
            ("page", "Join Our Mailing List", []),
            ("page", "Volunteer", []),
        ]),
        ("page", "Solar Education", [
            ("link", "Educational Resources", "/solar-education/"),
            ("page", "Solar Education Week", []),
        ]),
        ("page", "Media", [
            ("link", "Blog", "/media/"),
            ("page", "Press Room", []),
            ("page", "RE-volv in the News", []),
        ]),
        ("page", "Contact", [
            ("link", "Contact Us", "/contact/"),
        ]),
    ]

    def publish_page_for_parent(self, page, parent, user):
        """
        Publish a wagtail Page (or one of its subclasses, like RevolvCustomPage
        or RevolvLinkPage, as the given user as a child of the given parent.

        Note that the parent passed to this function may be None: if so, then the
        page will be published as a child of the root page of the site. Note that
        there is only one Site object that we care about here, since the RE-volv
        app doesn't have a notion of multiple "sites" to publish pages on - there's
        only one. If for some reason we needed more than one "site", then we would
        need to heavily modify this code.

        References:
            wagtail Site: https://github.com/torchbox/wagtail/blob/e937d7a1a32052966b6dfa9768168ea990f7916a/wagtail/wagtailcore/models.py#L52
            publishing a wagtail page: https://github.com/torchbox/wagtail/blob/e937d7a1a32052966b6dfa9768168ea990f7916a/wagtail/wagtailadmin/views/pages.py#L122
        """
        if parent:
            page_parent = parent
        else:
            only_site = Site.objects.all()[0]
            page_parent = only_site.root_page
        # this actually saves the page
        page_parent.add_child(instance=page)
        page.save_revision(user=user, submitted_for_moderation=False).publish()
        return page

    def publish_page(self, title, body, user, parent=None):
        """
        Publish a RevolvCustomPage with the given title and body, as the given
        user, under the given parent Page. If parent is None, publish under the
        root page of the site instead.
        """
        page = RevolvCustomPage(
            title=title,
            body=body,
            slug=title.lower().replace(" ", "-"),
            seo_title=title,
            show_in_menus=True,
            live=True
        )
        return self.publish_page_for_parent(page, parent, user)

    def publish_link_page(self, title, link_href, user, parent=None):
        """
        Publish a RevolvLinkPage with the given title and href, as the given
        user, under the given parent Page. If parent is None, publish under the
        root page of the site instead.
        """
        page = RevolvLinkPage(
            title=title,
            link_href=link_href,
            slug=title.lower().replace(" ", "-"),
            seo_title=title,
            show_in_menus=True,
            live=True
        )
        return self.publish_page_for_parent(page, parent, user)

    def recursively_seed_pages(self, pages, user, parent=None):
        """
        Given a list of pages to seed as in self.page_hierarchy, recursively
        publish the pages as the given user, under the given parent. If the
        parent is None, as in the other methods of this class, publish under
        the root page of the site instead.
        """
        for page_tuple in pages:
            page_type, title, data = page_tuple
            if page_type == "link":
                self.publish_link_page(title, data, user, parent)
            else:
                new_page = self.publish_page(title, "This is the body of the page", user, parent)
                self.recursively_seed_pages(data, user, new_page)

    def seed(self, quiet=False):
        """
        Publish all the pages in page_hierarchy as the administrator user.
        Because we have to publish as the administrator, this requires the
        revolvuserprofile seed spec to be run before this in order to succeed.
        """
        user = User.objects.get(username="administrator")
        self.recursively_seed_pages(self.page_hierarchy, user)

    def clear(self, quiet=False):
        """
        Clear all the RevolvCustomPages and RevolvLinkPages and reset the site
        root page. We need to reset the site root page because of how django-treebeard
        works. In order to keep a tree of related models, the parent Pages store
        meta information about their children, including paths.

        This means that we can't actually just delete all the Page models that
        we created in seed(): we instead have to do that AND delete the root page
        and reset it.

        References:
            wagtail Site model: https://github.com/torchbox/wagtail/blob/e937d7a1a32052966b6dfa9768168ea990f7916a/wagtail/wagtailcore/models.py#L52
            treebeard add_root() docs: https://tabo.pe/projects/django-treebeard/docs/1.61/api.html#treebeard.models.Node.add_root
        """
        try:
            only_site = Site.objects.all()[0]
            only_site.root_page.delete()
            new_root_page = Page.add_root(title="RE-volv Main Site Root")
            only_site.root_page = new_root_page
            only_site.save()
        except ObjectDoesNotExist as e:
            if not quiet:
                print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


class CMSSettingSeedSpec(SeedSpec):
    """
    Database seed specification for Wagtail settings. There are many parts
    of the app which are not full Wagtail CMS pages (and as such should not
    be seeded by the CMSPageSeedSpec) but should be editable: the titles of
    the homepage and auth pages, etc. See revolv.revolv_cms.models for
    documentation on Wagtail settings.

    The problem is that we currently define defaults for these settings, but
    they don't actually take effect without there being an object in the
    database for them. So, this seedspec looks at all the Wagtail settings
    and creates instances of them with the default values.

    We find all registered settings by looking at the Wagtailsettings registry.
    See https://bitbucket.org/takeflight/wagtailsettings/src/ab3e1fcf87db561417ca1fb65756d943153bdc3b/wagtailsettings/registry.py?at=master
    for info.
    """

    def seed(self, quiet=False):
        """Publish all settings with default values."""
        only_site = Site.objects.all()[0]
        for registered_settings_model in settings_registry.models:
            try:
                registered_settings_model.objects.create(site=only_site)
            except IntegrityError:
                if not quiet:
                    print "[Seed:Warning] Error in %s when trying to seed: %s already exists." % (
                        self.__class__.__name__, str(registered_settings_model)
                    )

    def clear(self, quiet=False):
        """Delete all registered settings."""
        for registered_settings_model in settings_registry.models:
            try:
                registered_settings_model.objects.all().delete()
            except ObjectDoesNotExist as e:
                if not quiet:
                    print "[Seed:Warning] Error in %s when trying to clear: %s" % (self.__class__.__name__, str(e))


SPECS_TO_RUN = (
    ("revolvuserprofile", RevolvUserProfileSeedSpec()),
    ("project", ProjectSeedSpec()),
    ("payment", PaymentSeedSpec()),
    ("cms", CMSPageSeedSpec()),
    ("cms_settings", CMSSettingSeedSpec())
)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--clear",
            action="store_true",
            dest="clear",
            default=False,
            help="Clear the seeded data instead of seeding it."
        ),
        make_option(
            "-s",
            "--spec",
            action="store",
            type="string",
            dest="spec"
        ),
        make_option(
            "--quiet",
            action="store_true",
            dest="quiet",
            default=False,
            help="Don't print warnings or logging information."
        ),
        make_option(
            "-l", "--list",
            action="store_true",
            dest="list",
            default=False,
            help="Show available seeds and exit."
        ),
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

        Options:
            --spec [spec name]: run only the specified SeedSpec
            --clear: clear the seed data instead of seed it
            --list: list available seed specs and stop.
            --quiet: don't print warnings, info notices, etc. Used mostly for keeping test
                output clean.
        """
        def log(message):
            """Log a message if the --quiet flag was not passed."""
            if not options["quiet"]:
                print message

        if options["list"]:
            log("[Seed:Info] The following seeds are available: ")
            log("[Seed:Info]    " + ", ".join([spec_data[0] for spec_data in SPECS_TO_RUN]))
            log("[Seed:Info] Done.")
            return

        if options["clear"]:
            verb = "Clearing"
        else:
            verb = "Seeding"

        specs_to_run = []
        if options["spec"]:
            spec = dict(SPECS_TO_RUN).get(options["spec"])
            if spec is not None:
                specs_to_run.append(spec)
            else:
                log("[Seed:Warning] Trying to run only spec %s, but it doesn't exist." % options["spec"])
        else:
            specs_to_run.extend([tup[1] for tup in SPECS_TO_RUN])

        log("[Seed:Info] %s objects from %i seed spec(s)..." % (verb, len(specs_to_run)))
        for spec in specs_to_run:
            if options["clear"]:
                spec.clear(quiet=options["quiet"])
            else:
                spec.seed(quiet=options["quiet"])
        log("[Seed:Info] Done!")
