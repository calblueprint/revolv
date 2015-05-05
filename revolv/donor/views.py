from django.contrib import messages
from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.project.models import Project


class DonorDashboardView(UserDataMixin, TemplateView):
    """
    Basic view for the Donor dashboard.
    """
    template_name = 'base/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if "password_change_success" in request.GET.keys():
            messages.success(request, "Awesome! Your password has been successfully changed.")

        return super(DonorDashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DonorDashboardView, self).get_context_data(**kwargs)

        project_dict = {}
        project_dict[ProjectGroup('My Projects', "donated")] = Project.objects.donated_projects(self.user_profile)
        context["project_dict"] = project_dict

        active = Project.objects.get_active()
        context["first_project"] = active[0] if active.count() > 0 else None
        context["role"] = "donor"
        context["donor_has_no_donated_projects"] = Project.objects.donated_projects(self.user_profile).count() == 0

        return context
