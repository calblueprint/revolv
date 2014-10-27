import datetime

import forms
from django.test import TestCase
from models import Project


# Create your tests here.


class ProjectTests(TestCase):
    """Project model tests."""

    def test_construct(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        # Note: there is a runtime warning of using a datetime
        # that is not timezone aware
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
        # Note: there is a runtime warning of using a datetime
        # that is not timezone aware
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


class ProjectFormTests(TestCase):
    """
    Project form tests
    """

    def test_project_form_is_valid(self):
        form_data = {}
        form_data['title'] = 'Hello'
        form_data['mission_statement'] = 'To be, or not to be'
        form_data['funding_goal'] = 35.5
        form_data['location'] = 'Honolulu'
        form_data['location_latitude'] = 0
        form_data['location_longitude'] = 0
        form_data['impact_power'] = 500.0
        form_data['end_date'] = '2024-10-25'
        form_data['video_url'] = 'https://www.youtube.com/watch?v=9bZkp7q19f0'
        form_data['cover_photo'] = 'http://i.imgur.com/2zMTZgi.jpg'
        form_data['org_start_date'] = '2014-10-10'
        form_data['org_name'] = 'What Up'
        form_data['org_about'] = 'We the best'

        bound_form = forms.ProjectForm(data=form_data)
        self.assertTrue(bound_form.is_valid())
