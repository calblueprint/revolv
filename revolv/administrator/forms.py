from django import forms
from revolv.payments.models import AdminAdjustment
from revolv.base.models import RevolvUserProfile
from revolv.project.models import Project

class AdjustmentForm(forms.ModelForm):
	
	queryset = RevolvUserProfile.objects.all()
	admin = forms.ModelChoiceField(queryset, widget=forms.HiddenInput())

	class Meta:
		model = AdminAdjustment

		widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Employee salaries'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'e.g. 12.0'}),
        }

        fields = (
            'name',
            'amount',
            'created_at',
        )

class AccountingFilterForm(forms.Form):

    queryset = Project.objects.all()
    project = forms.ModelChoiceField(queryset, label='Select project')

    class Meta:

        widgets = {
            'start_date': forms.DateInput(attrs={'label': 'Start date', 'placeholder': 'e.g. 03-2006', 'input_formats': '%m-%Y'}),
            'end_date': forms.DateInput(attrs={'label': 'End date', 'placeholder': 'e.g. 03-2006', 'input_formats': '%m-%Y'}),
        }

        fields = (
            'start_date',
            'end_date',
        )