from django import forms

from models import Project


class ProjectForm(forms.ModelForm):

    mission_statement = forms.CharField(widget=forms.Textarea)

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
            'org_start_date'
        )
