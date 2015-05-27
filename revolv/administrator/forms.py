from django import forms
from revolv.payments.models import AdminAdjustment
from revolv.project.models import Project

class AdjustmentForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 12.0'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'e.g. 12.0'}))
    created_at = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'e.g. 2006-03-03', 'input_formats': '%Y-%m-%d'}), initial='2015-02-02')
    cash_type = forms.ChoiceField(choices=['Cash in', 'Cash out'])

    class Meta:
        model = AdminAdjustment

        widgets = {

        }

        fields = (
            'name',
            'amount',
            'created_at',
            'cash_type'
        )

    def get_success_url(self):
        return reverse('administrator:accounting')