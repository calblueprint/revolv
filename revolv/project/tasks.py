import re
import tempfile
import urllib2

from bs4 import BeautifulSoup
from celery.task import task
from django.core.files import File
from models import Project
from utils import get_solar_csv_url


@task
def scrape():
    """Celery task to scrape for solar log csv data"""

    CSV_URL_REGEX = '(var svgsrc = ")[^"]+(";)'

    for project in Project.objects.all():

        # Scrape solar graphics page for csv url
        page = urllib2.urlopen(project.solar_url)
        soup = BeautifulSoup(page.read())
        content = soup.body.findAll(text=re.compile(CSV_URL_REGEX))[0]
        csv_id = content.split("&c=")[1].split("&mode=")[0]

        # For mode = 1,2,3 for daily, monthly, annual values
        for mode in range(1, 4):

            # Retrieve the webpage as a string
            response = urllib2.urlopen(get_solar_csv_url(csv_id, mode))
            csvstr = response.read()
            lines = csvstr.split("\r\n")

            # Write data to file field of project through temporary file
            temp = tempfile.TemporaryFile()
            for line in lines:
                temp.write(line + "\n")
            if mode == 1:
                project.daily_solar_data.save(csv_id, File(temp))
            elif mode == 2:
                project.monthly_solar_data.save(csv_id, File(temp))
            elif mode == 3:
                project.annual_solar_data.save(csv_id, File(temp))
            temp.close()
