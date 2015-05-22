from django import forms
from revolv.payments.models import AdminAdjustment
from revolv.base.models import RevolvUserProfile
from revolv.project.models import Project

class AdjustmentForm(forms.ModelForm):

    queryset = RevolvUserProfile.objects.all()
    admin = forms.ModelChoiceField(queryset, widget=forms.HiddenInput())
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 12.0'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'e.g. 12.0'}))
    created_at = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'e.g. 03-2006', 'input_formats': '%m-%Y'}))
    cash_type = forms.ChoiceField(choices=['Cash in', 'Cash out'])

    class Meta:
        model = AdminAdjustment