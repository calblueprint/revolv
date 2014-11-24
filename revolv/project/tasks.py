## /project_name/app_name/tasks.py

import re
import urllib2

from bs4 import BeautifulSoup
from celery.task import task
from models import Project
from utils import get_solar_csv_url


@task
def scrape():
    """Scrape for solar log csv data"""
    CSV_URL_REGEX = '(var svgsrc = ")[^"]+(";)'

    for project in Project.objects.all():

        # Scrape solar graphics page for csv url
        page = urllib2.urlopen(project.solar_url)
        soup = BeautifulSoup(page.read())
        content = soup.body.findAll(text=re.compile(CSV_URL_REGEX))[0]
        csv_id = content.split("&c=")[1].split("&mode=")[0]

        # Retrieve the webpage as a string
        response = urllib2.urlopen(get_solar_csv_url(csv_id, 0))
        csv = response.read()

        # Save the string to a file
        csvstr = str(csv).strip("b'")

        lines = csvstr.split("\\n")
        for line in lines:
            print line
