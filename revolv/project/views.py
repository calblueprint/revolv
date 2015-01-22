from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import FormView

from revolv.base.users import UserDataMixin
from revolv.payments.forms import CreditCardDonationForm
from revolv.project import forms
from revolv.project.models import Project


class CreateProjectView(CreateView):
    """
    The view to create a new project. Redirects to the homepage upon success.

    Accessed through /project/create
    """
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        new_project = Project.objects.create_from_form(form, self.request.user.revolvuserprofile)
        messages.success(self.request, new_project.title + ' has been created!')
        return super(CreateProjectView, self).form_valid(form)

    # sets context to be the create view, doesn't pass in the id
    def get_context_data(self, **kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['action'] = reverse('project:new')
        return context


class UpdateProjectView(UpdateView):
    """
    The view to update a project. It is the same view as creating a new
    project, though it prepopulates the existing field and passes in the
    project id. Redirects to the project page upon success.

    Accessed through /project/edit/{project_id}
    """
    model = Project
    template_name = 'project/edit_project.html'
    form_class = forms.ProjectForm

    def get_success_url(self):
        messages.success(self.request, 'Project details updated')
        return reverse('project:view', kwargs={'pk': self.get_object().id})

    # sets context to be the edit view by providing in the model id
    def get_context_data(self, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(**kwargs)
        context['action'] = reverse('project:edit',
                                    kwargs={'pk': self.get_object().id})
        return context


class ReviewProjectView(UpdateView):
    """
    The view to review a project. Shows the same view as ProjectView, but at
    the top, has a button group through which an ambassador or admin can
    update the project status.

    Accessed through /project/review/{project_id}
    """
    model = Project
    template_name = 'project/review_project.html'
    form_class = forms.ProjectStatusForm

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.get_object().id})

    # Checks the post request and updates the project_status
    def form_valid(self, form):
        project = self.object
        if '_approve' in self.request.POST:
            messages.success(self.request, project.title + ' has been approved')
            project.approve_project()
        elif '_propose' in self.request.POST:
            messages.success(self.request, project.title + ' is now pending approval')
            project.propose_project()
        elif '_deny' in self.request.POST:
            messages.error(self.request, project.title + ' has been denied')
            project.deny_project()
        elif '_complete' in self.request.POST:
            messages.success(self.request, project.title + ' has been completed')
            project.complete_project()
        return redirect(self.get_success_url())


class PostFundingUpdateView(UpdateView):
    """
    The view to review a project. Shows the same view as ProjectView, but at
    the top, has a button group through which an ambassador or admin can
    update the project status.

    Accessed through /project/review/{project_id}
    """
    model = Project
    template_name = 'project/post_funding_update.html'
    form_class = forms.PostFundingUpdateForm

    def get_success_url(self):
        return reverse('project:view', kwargs={'pk': self.get_object().id})


class ProjectView(UserDataMixin, DetailView):
    """
    The project view. Displays project details and allows for editing.

    Accessed through /project/{project_id}
    """
    model = Project
    template_name = 'project/project.html'

    def dispatch(self, request, *args, **kwargs):
        # always populate self.user, etc
        super_response = super(ProjectView, self).dispatch(request, *args, **kwargs)
        project = self.get_object()
        if (project.is_active or project.is_completed or
                (self.user.is_authenticated() and (project.has_owner(self.user_profile) or self.is_administrator))):
            return super_response
        else:
            return self.deny_access()


class CreateProjectDonationView(UserDataMixin, FormView):
    model = Project
    template_name = 'project/donate.html'
    form_class = CreditCardDonationForm

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        form.process_payment(project, self.user)
        return super(CreateProjectDonationView, self).form_valid(form)

    @property
    def success_url(self):
        return '/project/{0}'.format(self.kwargs.get('pk'))
