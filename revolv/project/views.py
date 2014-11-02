from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, UpdateView

import forms
from models import Project


# Create your views here.

"""
The view to create a new project. Redirects to the homepage upon success.

Accessed through /project/create
"""


class CreateProjectView(CreateView):
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('home')

    # sets context to be the create view, doesn't pass in the id
    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['action'] = reverse('project:new')
        return context


"""
The view to update a project. It is the same view as creating a new project,
though it prepopulates the existing field and passes in the project id.
Redirects to the project page upon success.

Accessed through /project/edit/{project_id}
"""


class UpdateProjectView(UpdateView):
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.get_object().id})

    # sets context to be the edit view by providing in the model id
    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        context['action'] = reverse('project:edit',
                                    kwargs={'pk': self.get_object().id})
        return context



"""
The project view. Displays project details and allows for editing.

Accessed through /project/{project_id}
"""


class ProjectView(DetailView):
    model = Project
    template_name = 'project/project.html'
