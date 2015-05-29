from django import forms
from revolv.payments.models import AdminAdjustment
from revolv.project.models import Project
from django.forms.models import modelform_factory


AdjustmentForm = modelform_factory(AdminAdjustment)