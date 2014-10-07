from django.test import TestCase
from models import Project
import datetime

# Create your tests here.

class ProjectTests(TestCase):
	"""Project model tests."""

	def test_construct(self):
		now = datetime.datetime.now()
		today = datetime.date.today()
		project = Project(
			funding_goal=50.0,
			title="Hello",
			video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
			impact_power=50.5,
			location="Berkeley",
			end_date=now,
			mission_statement="We do solar!",
			cover_photo="http://static.fjcdn.com/pictures/Why_05304a_2913881.jpg",
			org_start_date=today,
			actual_energy=25.5,
			amount_repaid=29.25,
		)
		self.assertEquals(
			project.funding_goal,
			50.0
		)
		self.assertEquals(
			project.title,
			"Hello"
		)
		self.assertEquals(
			project.video_url,
			"https://www.youtube.com/watch?v=9bZkp7q19f0"		
		)
		self.assertEquals(
			project.impact_power,
			50.5
		)
		self.assertEquals(
			project.location,
			"Berkeley"
		)
		self.assertEquals(
			project.end_date,
			now
		)
		self.assertEquals(
			project.project_status,
			'PR'
		)
		self.assertEquals(
			project.mission_statement,
			"We do solar!"
		)
		self.assertEquals(
			project.cover_photo,
			"http://static.fjcdn.com/pictures/Why_05304a_2913881.jpg"
		)
		self.assertEquals(
			project.org_start_date,
			today
		)
		self.assertEquals(
			project.actual_energy,
			25.5
		)
		self.assertEquals(
			project.amount_repaid,
			29.25
		)