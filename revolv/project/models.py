from django.db import models

# Create your models here.

class Project(models.Model):
    # or an integer field if we don't allow cents
    funding_goal = models.DecimalField(decimal_places=2)
    title = models.CharField(max_length=255)
    video_url = models.URLField(max_length=255)
    # power output of array in kilowatts
    impact_power = models.FloatField()
    # preferably use either GeoDjango or django-location-field
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    project_status = models.CharField(max_length=255)
    mission_statement = models.CharField(max_length=5000)
    # or an ImageField if we let them upload images
    cover_photo = models.URLField(max_length=255)
    org_start_date = models.DateField()
    # donor = models.ManyToManyField(Donor)
    # commented out until Donor model is implemented

    # ambassador = models.ForeignKey(Ambassador)
    # commented out until Ambassador model is implemented

    # energy produced in kilowatt hours
    actual_energy = models.FloatField()
    # or an integer field if we don't allow cents
    amount_repaid = models.DecimalField(decimal_places=2)
