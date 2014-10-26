from django.db import models


# Create your models here.


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
    funding_goal = models.DecimalField(max_digits=15, decimal_places=2)
    title = models.CharField(max_length=255)
    video_url = models.URLField(max_length=255)
    # power output of array in kilowatts
    impact_power = models.FloatField()
    location = models.CharField(max_length=255)
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
    end_date = models.DateTimeField()
    project_status = models.CharField(
        max_length=2,
        choices=PROJECT_STATUS_CHOICES,
        default=PROPOSED
    )
    mission_statement = models.CharField(max_length=5000)
    # or an ImageField if we let them upload images
    cover_photo = models.URLField(max_length=255)
    org_start_date = models.DateField()
    org_name = models.CharField(max_length=255)
    org_about = models.CharField(max_length=1000)

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
