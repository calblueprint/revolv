from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, UpdateView

import forms
from models import Project


# Create your views here.


class CreateProjectView(CreateView):
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('home')


class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('home')


class ProjectView(DetailView):
    model = Project
    template_name = 'project/project.html'
