from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.db.models import Sum

from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.payments.models import Payment
from revolv.project.models import Project, Category
from revolv.project.utils import aggregate_stats


def humanize_int(n):
    # NOTE: GPL licensed snipped c/o
    # https://github.com/localwiki/localwiki-backend-server/blob/master/localwiki/users/views.py#L47
    mag = 0
    if n < 1000:
        return str(n)
    while n>= 1000:
        mag += 1
        n /= 1000.0
    return '%.1f%s' % (n, ['', 'k', 'M', 'B', 'T', 'P'][mag])


def humanize_integers(d):
    for k in d:
        d[k] = humanize_int(int(d[k]))

def total_donations(profile):
    payments = Payment.objects.filter(entrant=profile, user=profile)
    if payments:
        return payments.aggregate(Sum('amount'))['amount__sum']
    else:
        return 0

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

        context['donated_projects'] = Project.objects.donated_projects(self.user_profile)
        statistics_dictionary = aggregate_stats(self.user_profile)
        statistics_dictionary['total_donated'] = total_donations(self.user_profile)
        statistics_dictionary['people_served'] = Project.objects.aggregate(n=Sum('people_affected'))['n']
        humanize_integers(statistics_dictionary)
        context['statistics'] = statistics_dictionary


        context['category_setter_url'] = reverse('dashboard_category_setter')
        context['categories'] = Category.objects.all().order_by('title')
        context['preferred_categories'] = self.user_profile.preferred_categories.all()

        return context
