from django import forms

from models import Project


class ProjectForm(forms.ModelForm):

    mission_statement = forms.CharField(widget=forms.Textarea)
    location_latitude = forms.DecimalField(widget=forms.HiddenInput())
    location_longitude = forms.DecimalField(widget=forms.HiddenInput())

    class Meta:
        model = Project
        # exclude = ('amount_repaid', 'actual_energy', 'project_status')
        fields = (
            'title',
            'mission_statement',
            'funding_goal',
            'location',
            'impact_power',
            'end_date',
            'video_url',
            'cover_photo',
            'org_name',
            'org_about',
            'org_start_date',
            'location_latitude',
            'location_longitude'
        )
