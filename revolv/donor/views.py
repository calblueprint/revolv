import datetime

from django.contrib import messages
from django.views.generic import TemplateView
from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.project.models import Project
from revolv.payments.models import AdminRepayment, AdminReinvestment, Payment, AdminAdjustment
from revolv.payments.utils import AccountingAggregator
from django.core.urlresolvers import reverse

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

class AccountingView(UserDataMixin, TemplateView):
    """
    View of the accounting page.
    """
    template_name = 'donor/accounting.html'

    def get_context_data(self, **kwargs):
        context = super(AccountingView, self).get_context_data(**kwargs)

        context['project_names'] = [p.title for p in Project.objects.all()]
        context['admin_repayments'] = AdminRepayment.objects.repayments()
        context['admin_reinvestments'] = AdminReinvestment.objects.reinvestments()
        context['donations'] = Payment.objects.donations()
        context['jsonurl'] = unicode(str(reverse('donor:accountingPartial')))

        context['clean_project_names'] = {}
        clean_project_names = context['clean_project_names']
        for p in context['project_names']:
            clean_name = AccountingAggregator().clean_project_name(p)
            clean_project_names[clean_name] = p

        return context

class AccountingPartialView(TemplateView):
    """
    A view that returns partial HTML of all relevant accounting data.
    This is queried by an AJAX request when creating the Accounting page.
    """

    start_date = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.now()
    project_filter = Project.objects.all()
    allProjects = Project.objects.all()
    template_name = 'base/partials/cash_flow_table.html'

    def updateFilterVariables(self, request):
        """
        Updates instance variables such as start_date, end_date, and project_filter
        based on the keys passed in.

        :args:
            keys: The request passed in to the AccountingPartialView
        """
        if 'start_date' in request:
            self.start_date = datetime.datetime.strptime(request['start_date'], '%Y-%m-%d')
        elif 'end_date' in request:
            self.end_date = datetime.datetime.strptime(request['end_date'], '%Y-%m-%d')
        elif 'project_choice' in request:
            if request['project_choice'] == 'all':
                self.project_filter = Project.objects.all()
            else:
                project_dict = {}
                for proj in self.allProjects:
                    name = proj.title
                    project_dict[AccountingAggregator().clean_project_name(name)] = name
                real_name = project_dict[request['project_choice']]
                self.project_filter = Project.objects.filter(title=real_name)

    def get_context_data(self, **kwargs):
        context = super(AccountingPartialView, self).get_context_data(**kwargs)
        revolv_earnings_rate = 0.07
        payment_service_fee_rate = 0.01
        filtered_dict = AccountingAggregator(self.start_date, self.end_date, self.project_filter, revolv_earnings_rate, payment_service_fee_rate).aggregate()
        context['data'] = filtered_dict
        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Updates the variables used to filter the data (such as start date, end date, and project)
        and then calls the inherited dispatch function.
        """
        self.updateFilterVariables(request.GET)
        normal_dispatch_dict = super(AccountingPartialView, self).dispatch(request, *args, **kwargs)
        return normal_dispatch_dict
