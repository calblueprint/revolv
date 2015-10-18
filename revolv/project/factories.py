import datetime

import factory
from revolv.project.models import Category, Project, ProjectUpdate


class ProjectFactory(factory.django.DjangoModelFactory):
    """
    Factory for default projects (drafted). Note: the cover_photo will be
    None for a default factory, because there doesn't seem to be a good way
    to import a default picture without having one in static files. Also, doing
    so would upload it to s3 every time a test used this factory.

    So, be careful about accessing cover_photo when using projects created
    by this factory.
    """
    class Meta:
        model = Project

    funding_goal = 50.0
    title = "Hello"
    tagline = "This project will be really cool."
    description = "This is a swaggy description of this project."
    video_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
    impact_power = 50.5
    location = "Berkeley"
    end_date = datetime.date.today() + datetime.timedelta(days=1)  # tomorrow
    mission_statement = "We do solar!"
    cover_photo = None
    org_name = "Power for Community Center"
    org_about = "Community Center is a center for communities."
    org_start_date = datetime.date.today() - datetime.timedelta(days=1)  # yesterday
    actual_energy = 25.5
    amount_repaid = 29.25
    ambassador = None
    created_by_user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    location_latitude = 42.0
    location_longitude = 42.0
    solar_url = "http://home.solarlog-web.net/1445.html",


class ProjectWithStartDateFactory(ProjectFactory):
    """
    Factory with a non-null start_date. Inherited by
    active and completed project factories.
    """
    start_date = datetime.date.today() - datetime.timedelta(days=1)  # yesterday


class ActiveProjectFactory(ProjectWithStartDateFactory):
    """Factory for default active projects."""
    project_status = Project.ACTIVE


class DraftedProjectFactory(ProjectFactory):
    """Factory for default drafted projects."""
    project_status = Project.DRAFTED


class ProposedProjectFactory(ProjectFactory):
    """Factory for default proposed projects."""
    project_status = Project.PROPOSED


class CompletedProjectFactory(ProjectWithStartDateFactory):
    """Factory for default completed projects."""
    project_status = Project.COMPLETED


class StagedProjectFactory(ProjectWithStartDateFactory):
    """Factory for default staged projects."""
    project_status = Project.STAGED


class ProjectFactories(object):
    base = ProjectFactory
    active = ActiveProjectFactory
    drafted = DraftedProjectFactory
    proposed = ProposedProjectFactory
    completed = CompletedProjectFactory
    staged = StagedProjectFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # note: we can't actually use default category names here, since newly created
    # factories might violate unique key constraints for category titles
    title = factory.Sequence(lambda n: 'Some Category %i' % n)


class CategoryFactories(object):
    base = CategoryFactory


class ProjectUpdateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectUpdate

    update_text = "This is an update"
    date = datetime.date.today()
    project = factory.SubFactory(ProjectFactory)


class ProjectUpdateFactories(object):
    base = ProjectUpdateFactory
