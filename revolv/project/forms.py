from django import forms
from models import Category, Project, ProjectUpdate, DonationLevel
from django.forms.models import inlineformset_factory
from models import Category, DonationLevel, Project


class ProjectForm(forms.ModelForm):
    """
    Form used for the Create and Update Project View. Controls what fields
    the user can access and their basic appearance to the user.
    """
    # sets the lat and long fields to hidden (clicking on the map updates them)
    location_latitude = forms.DecimalField(widget=forms.HiddenInput())
    location_longitude = forms.DecimalField(widget=forms.HiddenInput())
    # extra = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'id_extra'}))

    # generates options of categories and populates Multiple Choice field with options.
    options = [(category, category) for category in Category.valid_categories]
    categories_select = forms.MultipleChoiceField(choices=options, required=False)

    class Meta:
        model = Project
        # fields that need to be filled out
        localized_fields = ('__all__')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Other Avenues Food Cooperative'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'e.g. Power the future!'}),
            'funding_goal': forms.TextInput(attrs={'placeholder': 'e.g. $1000', 'min_value':0, 'decimal_places':2}),
            'impact_power': forms.NumberInput(attrs={'placeholder': 'e.g. 12.0'}),
            'end_date': forms.DateInput(attrs={'placeholder': 'e.g. 10/25/2006', 'input_formats': '%m/%d/%Y'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'e.g. youtube.com/url_to_video'}),
            'org_name': forms.TextInput(attrs={'placeholder': 'e.g. Other Avenues'}),
            'org_start_date': forms.DateInput(attrs={'placeholder': 'e.g. 10/25/2006', 'input_formats': '%m/%d/%Y'}),
            'org_about': forms.Textarea(attrs={'placeholder': 'e.g. Other Avenues is a worker-owned cooperative that seeks to maintain a thriving business while providing food and supplies for sustainable living, supporting organic and local farms and to serve as a model of workplace democracy for the community.'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. 3930 Judah Street San Francisco, CA 94122'}),
            'description': forms.Textarea(attrs={'placeholder': "e.g. The solar energy system will be a 36kW project that provides 33% of Other Avenue's electricity needs."}),
            'people_affected': forms.NumberInput(attrs={'placeholder': 'e.g. 12'}),
        }

        fields = (
            'title',
            'tagline',
            'funding_goal',
            'impact_power',
            'end_date',
            'video_url',
            'cover_photo',
            'org_name',
            'org_about',
            'org_start_date',
            'location',
            'location_latitude',
            'location_longitude',
            'categories_select',
            'description',
            'people_affected'
        )

    def clean_categories_select(self):
        """ This method processes the input from the hidden categories list field, which
        is a string of the comma separated values. It parses it and insures all the categories
        are valid, then converts it into an actual list.
        """
        data = self.cleaned_data['categories_select']
        categories_select = filter(None, data)
        # checks if a/ll the categories in it are valid
        for category in categories_select:
            if category not in Category.valid_categories:
                raise forms.ValidationError("You have entered an invalid category.")
        return categories_select


class ProjectStatusForm(forms.ModelForm):
    """
    An empty form, used so that one can update the project status through
    the ReviewProjectView
    """
    class Meta:
        model = Project
        # fields that need to be filled out, empty on purpose
        fields = ()

class EditProjectUpdateForm(forms.ModelForm):
    """ 
    A form used to edit updates about a project
    """
    class Meta:
        model = ProjectUpdate
        
        widgets = {
            'update_text': forms.Textarea(attrs={'placeholder': 'e.g. Thank you for all the support! The project has been going extremely well. These are the milestones we have hit so far, and this is what we plan to do in the near future.'}),
        }

        fields = (
            'update_text',
        )

def make_donation_level_formset(extra):
    ProjectDonationLevelFormSet = inlineformset_factory(Project, DonationLevel, extra=extra)
    return ProjectDonationLevelFormSet
