import csv
import json
import datetime
import urllib

from django.http import HttpResponse, JsonResponse
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


class AccountingJSONView(View):
    """
    A view that returns a JsonResponse of all relevant accounting data.
    This is queried by an AJAX request when creating the Accounting page.

    The data is structured as shown below:
    data = {
        'cash_in': {
            'adjustments': {
                '2015-01-01': {
                    'Power Community Dance Studio': {
                        'total': 5,
                        'transactions': {
                            'income': 3,
                            'other income': 2,
                        },
                    },
                },
            },
            'donations': {
                '2015-01-01': {
                    'Power Community Dance Studio': {
                        'total': 5,
                        'payment_service_fees': 3,
                        'retained_donations': 2,
                    },
                },
            },
            'repayments': {
                '2015-01-01': {
                    'Power Community Dance Studio': {
                        'total': 5,
                        'revolv_earnings': 3,
                        'retained_ROI': 2,
                    },
                },
            },
        },
        'cash_out': {
            'adjustments': {
                '2015-01-01': {
                    'Power Community Dance Studio': {
                        'total': 5,
                        'transactions': {
                            'salaries': 3,
                            'other expenses': 2,
                        },
                    },
                },
            },
            'reinvestments': {
                'total': 5,
            },
        },
        'date_info': {
            'date_list': [
                '2015-01-01',
                '2015-02-01',
                '2015-03-01',
                ],
            'start_date': '2015-01-01',
            'end_date': '2015-03-01',
        },
        'project_names': [
            'Power Community Dance Studio',
        ],
        'cash_in_adjustment_names': [
            'income',
            'other income',
        ],
        'cash_out_adjustment_names': [
            'salaries',
            'other expenses',
        ],
        'cash_balances': {
            "2015-03-01": {
              "net_cash_out": 50,
              "net_cash_in": 0,
              "change_in_cash": -50,
              "beginning_cash_balance": -5000,
              "final_cash_balance": -5050
        },
    }
    """

    start_date = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.now()
    project_filter = Project.objects.all()
    allProjects = Project.objects.all()

    """
    Updates instance variables such as start_date, end_date, and project_filter
    based on the keys passed in.

    :args:
        keys: The request passed in to the AccountingJSONView
    """
    def updateFilterVariables(self, request):

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
                    project_dict[AccountingAggregator.clean_project_name(name)] = name
                real_name = project_dict[request['project_choice']]
                self.project_filter = Project.objects.filter(title=real_name)

    """
    Creates and returns a JsonResponse.
    """
    def dispatch(self, request, *args, **kwargs):
        request = request.GET
        self.updateFilterVariables(request)
        revolv_earnings_rate = 0.07
        payment_service_fee_rate = 0.01
        filtered_dict = AccountingAggregator(self.start_date, self.end_date, self.project_filter, revolv_earnings_rate, payment_service_fee_rate).aggregate()
        return JsonResponse(filtered_dict)


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
