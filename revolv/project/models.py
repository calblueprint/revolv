from django.db import models

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

"""
Project model. Stores basic metadata, information about the project,
donations, energy impact, goals, and info about the organization.
"""


class Project(models.Model):
    ACCEPTED = 'AC'
    PROPOSED = 'PR'
    COMPLETED = 'CO'
    BUILDING = 'BU'
    PROJECT_STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (PROPOSED, 'Proposed'),
        (COMPLETED, 'Completed'),
        (BUILDING, 'Building'),
    )
    funding_goal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text = 'How much do you aim to raise for this project?'
    )
    title = models.CharField(
        max_length=255,
        help_text = 'How would you like to title this project?'
    )
    video_url = models.URLField(
        'Video URL',
        max_length=255,
        blank = True,
        help_text = 'Optional: Link to a Youtube video about the project or community.'
    )
    # power output of array in kilowatts
    impact_power = models.FloatField(
        'Expected KilloWatt Output',
        help_text = 'What is the expected output in killowatts of the proposed solar array.'
    )
    location = models.CharField(
        'Organization Address',
        max_length=255,
        help_text = 'What is the address of the organization where the solar panels will be installed?'
    )
    # latitude and longitude of the organization location
    location_latitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        default=0.0
    )
    location_longitude = models.DecimalField(
        max_digits=17,
        decimal_places=14,
        default=0.0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField(
        help_text = 'When will this crowdfunding project end?'
    )
    project_status = models.CharField(
        max_length=2,
        choices=PROJECT_STATUS_CHOICES,
        default=PROPOSED
    )
    cover_photo = ProcessedImageField(
        upload_to='covers',
        processors=[ResizeToFill(1200, 500)],
        format='JPEG',
        options={'quality': 80},
        default=None,
        help_text = 'Choose a beautiful high resolution image to represent this project.'
    )
    preview_photo = ImageSpecField(
        source='cover_photo',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 80},
    )
    org_start_date = models.DateField(
        'Organization Founding Date',
        blank = True,
        null = True,
        help_text = 'When was the organization being helped established?'
    )
    org_name = models.CharField(
        'Organization Name',
        max_length=255,
        help_text = 'What is the name of the organizatoin being helped?'
    )
    mission_statement = models.TextField(
        'Organization Mission',
        help_text = 'What is the mission statement of the organization being helped by this project?'
    )
    org_about = models.TextField(
        'Organization Description',
        help_text = 'Elaborate more about the organization, what it does, who it serves, etc.'
    )

    # commented out until Donor model is implemented
    # donor = models.ManyToManyField(Donor)

    # commented out until Ambassador model is implemented
    # ambassador = models.ForeignKey(Ambassador)

    # energy produced in kilowatt hours
    actual_energy = models.FloatField(default=0.0)
    amount_repaid = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0
    )


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    projects = models.ManyToManyField(Project)
