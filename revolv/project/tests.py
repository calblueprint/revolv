import datetime

from django.test import TestCase

import forms
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
        )
        p.save()
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")
