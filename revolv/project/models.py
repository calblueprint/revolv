from itertools import chain

from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from revolv.base.models import RevolvUserProfile


class ProjectManager(models.Manager):
    """
    Manager for running custom operations on the Projects.
    """

    def get_featured(self, num_projects, queryset=None):
        """ Get num_projects amount of active projects. If we don't have
        enough active projects, then we retrieve completed projects. This
        function may return fewer projects than requested if not enough exist.

        :num_projects: Number of projects to be retrieved
        :queryset: The queryset in which to search for projects
        :return: A list of featured project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        featured_projects = queryset.filter(
            project_status=Project.ACTIVE).order_by(
            'end_date')[:num_projects]
        if featured_projects.count() < num_projects:
            num_completed_needed = num_projects - featured_projects.count()
            completed_projects = queryset.filter(
                project_status=Project.COMPLETED).order_by(
                'end_date')[:num_completed_needed]
            return list(chain(featured_projects, completed_projects))
        else:
            return featured_projects

    def get_completed(self, queryset=None):
        """ Gets all the projects that have been completed funding.

        :queryset: The queryset in which to search for projects
        :return: A list of completed project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        completed_projects = queryset.filter(
            project_status=Project.COMPLETED).order_by(
            'end_date')
        return completed_projects

    def get_active(self, queryset=None):
        """ Gets all the projects that have been active to go into funding.

        :queryset: The queryset in which to search for projects
        :return: A list of active project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        active_projects = queryset.filter(
            project_status=Project.ACTIVE).order_by(
            'end_date')
        return active_projects

    def get_proposed(self, queryset=None):
        """ Gets all the projects that are currently in review (proposed).

        :queryset: The queryset in which to search for projects
        :return: A list of in review project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        proposed_projects = queryset.filter(
            project_status=Project.PROPOSED).order_by(
            'updated_at')
        return proposed_projects

    def get_drafted(self, queryset=None):
        """ Get all the projects that are drafted in the queryset.

        :queryset: The queryset in which to search for projects
        :return: A list of in review project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        drafted_projects = queryset.filter(
            project_status=Project.DRAFTED).order_by(
            'updated_at')
        return drafted_projects

    def owned_projects(self, user_profile):
        """ Get all projects owned by a RevolvUserProfile.

        :user: The user of interest
        :return: A list of projects for which user's RevolvUserProfile
        is the ambassador
        """
        return Project.objects.filter(ambassador=user_profile)

    def create_from_form(self, form, ambassador):
        project = form.save(commit=False)
        project.ambassador = ambassador
        project.save()
        return project


class Project(models.Model):
    """
    Project model. Stores basic metadata, information about the project,
    donations, energy impact, goals, and info about the organization.
    """
    ACTIVE = 'AC'
    PROPOSED = 'PR'
    COMPLETED = 'CO'
    DRAFTED = 'DR'
    PROJECT_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PROPOSED, 'Proposed'),
        (COMPLETED, 'Completed'),
        (DRAFTED, 'Drafted'),
    )
    funding_goal = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='How much do you aim to raise for this project?'
    )
    title = models.CharField(
        max_length=255,
        help_text='How would you like to title this project?'
    )
    video_url = models.URLField(
        'Video URL',
        max_length=255,
        blank=True,
        help_text='Optional: Link to a Youtube video about the project or community.'
    )
    # power output of array in kilowatts
    impact_power = models.FloatField(
        'Expected Killowatt Output',
        help_text='What is the expected output in killowatts of the proposed solar array?'
    )
    location = models.CharField(
        'Organization Address',
        max_length=255,
        help_text='What is the address of the organization where the solar panels will be installed?'
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
        help_text='When will this crowdfunding project end?'
    )
    project_status = models.CharField(
        max_length=2,
        choices=PROJECT_STATUS_CHOICES,
        default=DRAFTED
    )
    cover_photo = ProcessedImageField(
        upload_to='covers',
        processors=[ResizeToFill(1200, 500)],
        format='JPEG',
        options={'quality': 80},
        default=None,
        help_text='Choose a beautiful high resolution image to represent this project.'
    )
    preview_photo = ImageSpecField(
        source='cover_photo',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 80},
    )
    org_start_date = models.DateField(
        'Organization Founding Date',
        blank=True,
        null=True,
        help_text='When was the organization being helped established?'
    )
    org_name = models.CharField(
        'Organization Name',
        max_length=255,
        help_text='What is the name of the organization being helped?'
    )
    mission_statement = models.TextField(
        'Organization Mission',
        help_text='What is the mission statement of the organization being helped by this project?'
    )
    org_about = models.TextField(
        'Organization Description',
        help_text='Elaborate more about the organization, what it does, who it serves, etc.'
    )

    ambassador = models.ForeignKey(RevolvUserProfile)

    # energy produced in kilowatt hours
    actual_energy = models.FloatField(default=0.0)
    amount_repaid = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0
    )
    internal_rate_return = models.DecimalField(
        'Internal Rate of Return',
        max_digits=6,
        decimal_places=3,
        default=0.0,
        help_text='The internal rate of return for this project.'
    )

    objects = ProjectManager()

    def approve_project(self):
        self.project_status = Project.ACTIVE
        self.save()
        return self

    def propose_project(self):
        self.project_status = Project.PROPOSED
        self.save()
        return self

    def deny_project(self):
        self.project_status = Project.DRAFTED
        self.save()
        return self

    def complete_project(self):
        self.project_status = Project.COMPLETED
        self.save()
        return self


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    projects = models.ManyToManyField(Project)
