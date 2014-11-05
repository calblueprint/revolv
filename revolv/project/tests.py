import datetime

from django.test import TestCase

from models import Project


# Create your tests here.


class ProjectTests(TestCase):
    """Project model tests."""

    def test_construct(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        Project.objects.create(
            funding_goal=50.0,
            title="Hello",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            impact_power=50.5,
            location="Berkeley",
            end_date=tomorrow,
            mission_statement="We do solar!",
            cover_photo="http://i.imgur.com/2zMTZgi.jpg",
            org_start_date=yesterday,
            actual_energy=25.5,
            amount_repaid=29.25,
            ambassador_id=1,
        )
        testProject = Project.objects.get(title="Hello")
        self.assertEqual(testProject.mission_statement, "We do solar!")
        self.assertEqual(testProject.impact_power, 50.5)

    def test_save_and_query(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        p = Project(
            funding_goal=20.0,
            title="Hello",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            impact_power=50.5,
            location="San Francisco",
            end_date=tomorrow,
            mission_statement="Blueprint!",
            cover_photo="http://i.imgur.com/2zMTZgi.jpg",
            org_start_date=yesterday,
            actual_energy=25.5,
            amount_repaid=29.25,
            ambassador_id=1,
        )
        p.save()
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")


class ProjectManagerTests(TestCase):
    """Tests for the Project manager"""
    fixtures = ['project', 'user']

    def test_get_featured(self):
        context = Project.objects.get_featured(1)
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")
        context = Project.objects.get_featured(10)
        self.assertEqual(len(context), 2)
        self.assertEqual(context[1].org_name, "Comoonity Dairy")

    def test_get_completed(self):
        context = Project.objects.get_completed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Comoonity Dairy")

    def test_get_accepted(self):
        context = Project.objects.get_accepted()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")

    def test_get_proposed(self):
        context = Project.objects.get_proposed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Educathing")

    def test_get_drafted(self):
        context = Project.objects.get_drafted()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Fire Emblem")

    def test_get_drafted(self):
        context = Project.objects.get_drafted()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Fire Emblem")
