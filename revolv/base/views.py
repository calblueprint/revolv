from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """Website home page. THIS VIEW IS INCOMPLETE. UPDATE DOCSTRING
    WHEN COMPLETED."""
    template_name = 'base/home.html'

