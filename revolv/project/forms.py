from django import forms

from models import Project


class ProjectForm(forms.ModelForm):
    """
    Form used for the Create and Update Project View. Controls what fields
    the user can access and their basic appearance to the user.
    """

    # sets the lat and long fields to hidden (clicking on the map updates them)
    location_latitude = forms.DecimalField(widget=forms.HiddenInput())
    location_longitude = forms.DecimalField(widget=forms.HiddenInput())

    class Meta:
        model = Project
        # fields that need to be filled out
        fields = (
            'title',
            'mission_statement',
            'funding_goal',
            'impact_power',
            'end_date',
            'video_url',
            'solar_url',
            'cover_photo',
            'org_name',
            'org_about',
            'org_start_date',
            'location',
            'location_latitude',
            'location_longitude'
        )


class ProjectStatusForm(forms.ModelForm):
    """
    An empty form, used so that one can update the project status through
    the ReviewProjectView
    """
    class Meta:
        model = Project
        # fields that need to be filled out, empty on purpose
        fields = ()
