from django.core.urlresolvers import reverse
from django.shortcuts import redirect
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

    def form_valid(self, form):
        Project.objects.create_from_form(form, self.request.user)
        return super(CreateProjectView, self).form_valid(form)

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
The view to review a project. Shows the same view as ProjectView, but at
the top, has a button group through which an ambassador or admin can
update the project status.

<<<<<<< HEAD
=======

>>>>>>> FETCH_HEAD
Accessed through /project/review/{project_id}
"""


class ReviewProjectView(UpdateView):
    model = Project
    template_name = 'project/review_project.html'
    form_class = forms.ProjectStatusForm

    def get_success_url(self):
        return reverse('dashboard')

    """
    Checks the post request and updates the project_status
    """
    def form_valid(self, form):
        project = self.object
        if '_approve' in self.request.POST:
<<<<<<< HEAD
            project.approve_project()
        elif '_propose' in self.request.POST:
            project.propose_project()
        elif '_deny' in self.request.POST:
            project.deny_project()
        elif '_complete' in self.request.POST:
            project.complete_project()
=======
            Project.objects.approve_project(project)
        elif '_propose' in self.request.POST:
            Project.objects.propose_project(project)
        elif '_deny' in self.request.POST:
            Project.objects.deny_project(project)
        elif '_complete' in self.request.POST:
            Project.objects.complete_project(project)
>>>>>>> FETCH_HEAD
        return redirect(self.get_success_url())


"""
The project view. Displays project details and allows for editing.

Accessed through /project/{project_id}
"""


class ProjectView(DetailView):
    model = Project
    template_name = 'project/project.html'
