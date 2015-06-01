import csv
import json
import datetime
import urllib

from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, View
from revolv.base.models import RevolvUserProfile
from revolv.base.users import UserDataMixin
from revolv.base.views import BaseStaffDashboardView
from revolv.payments.models import AdminRepayment, AdminReinvestment, Payment, AdminAdjustment
from revolv.administrator.forms import AdjustmentForm
from revolv.project.models import Project
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse
from revolv.payments.utils import AccountingAggregator

class AdministratorDashboardView(BaseStaffDashboardView):
    """
    Basic view for the Administrator dashboard. Shows the list of projects that this
    ambassador owns.
    """
    template_name = 'base/dashboard.html'
    role = "admin"


class AdministratorEmailView(UserDataMixin, TemplateView):
    """View for the list of newsletter subscribers for the dashboard.
    """
    template_name = 'administrator/email.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorEmailView, self).get_context_data(**kwargs)

        user_emails = RevolvUserProfile.objects.get_subscribed_to_newsletter().values_list("user__email", flat=True)
        context['subscribed_user_emails'] = user_emails
        return context


class AdministratorAccountingView(UserDataMixin, TemplateView):
    """
    View of the administrator accounting page.
    """
    template_name = 'administrator/accounting.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorAccountingView, self).get_context_data(**kwargs)

        context['project_names'] = [p.title for p in Project.objects.all()]
        context['admin_repayments'] = AdminRepayment.objects.repayments()
        context['admin_reinvestments'] = AdminReinvestment.objects.reinvestments()
        context['donations'] = Payment.objects.donations()
        context['jsonurl'] = unicode(str(reverse('administrator:accountingJSON')))

        context['clean_project_names'] = {}
        clean_project_names = context['clean_project_names']
        for p in context['project_names']:
            clean_name = AccountingAggregator().clean_project_name(p)
            clean_project_names[clean_name] = p

        return context

class AccountingJSONView(TemplateView):
    """
    A view that returns a JsonResponse of all relevant accounting data.
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
            keys: The request passed in to the AccountingJSONView
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
        context = super(AccountingJSONView, self).get_context_data(**kwargs)
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
        normal_dispatch_dict = super(AccountingJSONView, self).dispatch(request, *args, **kwargs)
        return normal_dispatch_dict

class AdministratorAddAdjustmentView(CreateView):
    
    model = AdminAdjustment
    template_name = 'administrator/adjustment.html'

    def get_success_url(self):
        return reverse('administrator:accounting')

    def get_form_kwargs(self):
        kwargs = super(AdministratorAddAdjustmentView, self).get_form_kwargs()
        self.form = AdjustmentForm()
        return kwargs

def admin_email_csv_download(request):
    """View for downloading the list of newsletter subscribers as a csv file.
    Accessed via AdministratorEmailView.
    """
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'

    # gets users who are subscribed to the newsletter ordered by signup date
    subscribed_to_newsletter_ordered = RevolvUserProfile.objects.get_subscribed_to_newsletter()

    writer = csv.writer(response)
    writer.writerow(['Email', 'FirstName', 'LastName', 'DateJoined'])

    for revolvuserprofile in subscribed_to_newsletter_ordered:
        writer.writerow([revolvuserprofile.user.email, revolvuserprofile.user.first_name, revolvuserprofile.user.last_name, revolvuserprofile.user.date_joined])

    return response
