import datetime

import factory
from revolv.project.models import Category, Project


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    funding_goal = 50.0
    title = "Hello"
    tagline = "This project will be really cool."
    video_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    impact_power = 50.5
    location = "Berkeley"
    end_date = datetime.date.today() - datetime.timedelta(days=1)  # tomorrow
    mission_statement = "We do solar!"
    cover_photo = "http://i.imgur.com/2zMTZgi.jpg"
    org_start_date = datetime.date.today() + datetime.timedelta(days=1)  # today
    actual_energy = 25.5
    amount_repaid = 29.25
    ambassador = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")


class ProjectFactories(object):
    base = ProjectFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Iterator(Category.valid_categories)


class CategoryFactories(object):
    base = CategoryFactory
