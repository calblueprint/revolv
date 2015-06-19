from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.project.models import Project, Category


class DonorDashboardView(UserDataMixin, TemplateView):
    """
    Basic view for the Donor dashboard.
    """
    template_name = 'base/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if "password_change_success" in request.GET.keys():
            messages.success(request, "Awesome! Your password has been successfully changed.")

        return super(DonorDashboardView, self).dispatch(request, *args, **kwargs)

    def make_statistics_dictionary(self):
        stat_dict = {}
        stat_dict['project_count'] = Project.objects.donated_projects(self.user_profile).count()
        stat_dict['repayments'] = Payment.objects.repayment_fragments(user=self.user_profile).aggregate(Sum('amount'))['amount__sum'] or 0
        return stat_dict

    def get_context_data(self, **kwargs):
        context = super(DonorDashboardView, self).get_context_data(**kwargs)

        project_dict = {}
        project_dict[ProjectGroup('My Projects', "donated")] = Project.objects.donated_projects(self.user_profile)
        context["project_dict"] = project_dict

        active = Project.objects.get_active()
        context["first_project"] = active[0] if active.count() > 0 else None
        context["role"] = "donor"
        context["donor_has_no_donated_projects"] = Project.objects.donated_projects(self.user_profile).count() == 0

        context['donated_projects'] = Project.objects.donated_projects(self.user_profile)
        statistics_dictionary = self.make_statistics_dictionary()
        context['statistics'] = statistics_dictionary

        context['category_setter_url'] = reverse('dashboard_category_setter')
        context['categories'] = Category.objects.all().order_by('title')
        context['preferred_categories'] = self.user_profile.preferred_categories.all()

        return context
