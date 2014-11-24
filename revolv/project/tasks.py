## /project_name/app_name/tasks.py

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
        csvstr = response.read()
        lines = csvstr.split("\r\n")

        # Write data to CSV of project through temporary file
        temp = tempfile.TemporaryFile()
        for line in lines:
            temp.write(line + "\n")
        temp.seek(0)
        for line in temp.readlines():
            print line
        project.solar_data.save(csv_id, File(temp))
        temp.close()
