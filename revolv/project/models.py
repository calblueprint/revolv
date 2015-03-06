import datetime
from itertools import chain

from django.core.urlresolvers import reverse
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import Payment


# class ProjectFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = "revolv.project.Project"

#     funding_goal = 50.0
#     title = "Hello"
#     video_url = "https://www.youtube.com/watch?v=9bZkp7q19f0"
#     impact_power = 50.5
#     location = "Berkeley"
#     end_date = datetime.date.today() - datetime.timedelta(days=1) # tomorrow
#     mission_statement = "We do solar!"
#     cover_photo = "http://i.imgur.com/2zMTZgi.jpg"
#     org_start_date = datetime.date.today() + datetime.timedelta(days=1)  # today
#     actual_energy = 25.5
#     amount_repaid = 29.25

# class ProjectFactories(object):
#     base = ProjectFactory

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
            project_status=Project.COMPLETED
        ).order_by('end_date')
        return completed_projects

    def get_active(self, queryset=None):
        """ Gets all the projects that have been active to go into funding.

        :queryset: The queryset in which to search for projects
        :return: A list of active project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        active_projects = queryset.filter(
            project_status=Project.ACTIVE
        ).order_by('end_date')
        return active_projects

    def get_proposed(self, queryset=None):
        """ Gets all the projects that are currently in review (proposed).

        :queryset: The queryset in which to search for projects
        :return: A list of in review project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        proposed_projects = queryset.filter(
            project_status=Project.PROPOSED
        ).order_by('updated_at')
        return proposed_projects

    def get_drafted(self, queryset=None):
        """ Get all the projects that are drafted in the queryset.

        :queryset: The queryset in which to search for projects
        :return: A list of in review project objects
        """
        if queryset is None:
            queryset = super(ProjectManager, self).get_queryset()
        drafted_projects = queryset.filter(
            project_status=Project.DRAFTED
        ).order_by('updated_at')
        return drafted_projects

    def owned_projects(self, user_profile):
        """ Get all projects owned by a RevolvUserProfile.

        :user: The user of interest
        :return: A list of projects for which user's RevolvUserProfile
        is the ambassador
        """
        return Project.objects.filter(ambassador=user_profile)

    def donated_projects(self, user_profile):
        """
        :return: Projects to which this RevolvUserProfile has donated
        """
        return user_profile.project_set.all()

    def create_from_form(self, form, ambassador):
        """ Creates project from form and sets ambassador to a RevolvUserProfile.

        :form: The form
        :ambassador: The RevolvUserProfile of the ambassador of the project
        :return: Project created and saved
        """
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
    LESS_THAN_ONE_DAY_LEFT_STATEMENT = "only hours left"
    NO_DAYS_LEFT_STATEMENT = "deadline reached"

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
    # solar log graphics url
    solar_url = models.URLField(
        'Solar Log Graphics URL',
        max_length=255,
        blank=True,
        help_text='This can be found by going to http://home.solarlog-web.net/, going to the \
        solar log profile for your site, and clicking on the Graphics sub-page. Copy and paste \
        the URL in the address bar into here.'
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

    donors = models.ManyToManyField(RevolvUserProfile)

    ambassador = models.ForeignKey(RevolvUserProfile, related_name='ambassador')

    # energy produced in kilowatt hours
    actual_energy = models.FloatField(default=0.0)
    internal_rate_return = models.DecimalField(
        'Internal Rate of Return',
        max_digits=6,
        decimal_places=3,
        default=0.0,
        help_text='The internal rate of return for this project.'
    )
    post_funding_updates = models.TextField(
        'Updates After Completion',
        help_text='Add any post project completion updates you want to let your backers know about.',
        null=True
    )

    # solar data csv files
    daily_solar_data = models.FileField(null=True, upload_to="projects/daily/")
    monthly_solar_data = models.FileField(null=True, upload_to="projects/monthly/")
    annual_solar_data = models.FileField(null=True, upload_to="projects/annual/")

    objects = ProjectManager()
    # factories = ProjectFactories

    def has_owner(self, ambassador):
        return self.ambassador == ambassador

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

    def mark_as_incomplete_project(self):
        self.project_status = Project.ACTIVE
        self.save()
        return self

    def get_absolute_url(self):
        return reverse("project:view", kwargs={"pk": str(self.pk)})

    @property
    def amount_donated(self):
        """
        :return: the current total amount that has been donated to this project,
            as a float
        """
        result = Payment.objects.donations(project=self).aggregate(
            models.Sum('amount')
        )["amount__sum"]
        if result is None:
            return 0.0
        return result

    @property
    def amount_left(self):
        """
        :return: the current amount of money needed for this project to
            reach its goal, as a float.
        """
        amt_left = float(self.funding_goal) - self.amount_donated
        if amt_left < 0:
            return 0.0
        return amt_left

    @property
    def amount_repaid(self):
        """
        :return: the current amount of money repaid by the project to RE-volv.
        """
        return Payment.objects.repayments(project=self).aggregate(models.Sum('amount'))["amount__sum"] or 0.0

    @property
    def rounded_amount_left(self):
        """
        :return: The amount needed to complete this project, floored to the nearest
            dollar.

        Note: if for some reason the amount left is negative, this will perform a
        ceiling operation instead of a floor, but that should never happen.
        """
        return int(self.amount_left)

    @property
    def partial_completeness(self):
        """
        :return: a float between 0 and 1, representing the completeness of this
            project with respect to its goal (1 if exactly the goal amount, or
            more, has been donated, 0 if nothing has been donated).
        """
        ratio = self.amount_donated / float(self.funding_goal)
        return min(ratio, 1.0)

    def partial_completeness_as_js(self):
        return unicode(self.partial_completeness)

    @property
    def days_until_end(self):
        return (datetime.date.today() - self.end_date).days

    @property
    def days_left(self):
        return max(self.days_until_end, 0)

    def formatted_days_left(self):
        days_left = self.days_until_end
        if days_left == 1:
            return "1 day left"
        if days_left == 0:
            return self.LESS_THAN_ONE_DAY_LEFT_STATEMENT
        if days_left < 0:
            return self.NO_DAYS_LEFT_STATEMENT
        return unicode(days_left) + " days left"

    @property
    def is_active(self):
        return self.project_status == Project.ACTIVE

    @property
    def is_proposed(self):
        return self.project_status == Project.PROPOSED

    @property
    def is_drafted(self):
        return self.project_status == Project.DRAFTED

    @property
    def is_completed(self):
        return self.project_status == Project.COMPLETED


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    projects = models.ManyToManyField(Project)
