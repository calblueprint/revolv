from django.test import TestCase
from models import Project
import datetime

# Create your tests here.

class ProjectTests(TestCase):
	"""Project model tests."""

	def test_construct(self):
		yesterday = datetime.date.today() - datetime.timedelta(days=1)
		# Note: there is a runtime warning of using a datetime
		# that is not timezone aware
		tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
		Project.objects.create(
			funding_goal=50.0,
			title="Hello",
			video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
			impact_power=50.5,
			location="Berkeley",
			end_date=tomorrow,
			mission_statement="We do solar!",
			cover_photo="http://static.fjcdn.com/pictures/Why_05304a_2913881.jpg",
			org_start_date=yesterday,
			actual_energy=25.5,
			amount_repaid=29.25,
		)
		testProject = Project.objects.get(title="Hello")
		self.assertEqual(testProject.mission_statement, "We do solar!")
		self.assertEqual(testProject.impact_power, 50.5)