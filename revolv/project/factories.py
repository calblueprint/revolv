import datetime

import factory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "revolv.project.Project"

    funding_goal = 50.0
    title = "Hello"
    video_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    impact_power = 50.5
    location = "Berkeley"
    end_date = datetime.date.today() - datetime.timedelta(days=1)  # tomorrow
    mission_statement = "We do solar!"
    cover_photo = "http://i.imgur.com/2zMTZgi.jpg"
    org_start_date = datetime.date.today() + datetime.timedelta(days=1)  # today
    actual_energy = 25.5
    amount_repaid = 29.25


class ProjectFactories(object):
    base = ProjectFactory
