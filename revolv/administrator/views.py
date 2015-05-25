import csv
import json
import datetime

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, FormView, View
from revolv.base.models import RevolvUserProfile
from revolv.base.users import UserDataMixin
from revolv.base.views import BaseStaffDashboardView
from revolv.payments.models import AdminRepayment, AdminReinvestment, Payment, AdminAdjustment
from revolv.administrator.forms import AdjustmentForm
from revolv.project.models import Project
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.urlresolvers import reverse

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


class AdministratorAccountingView(TemplateView):
    """View of the administrator accounting page.
    """
    template_name = 'administrator/accounting.html'

    def get_context_data(self, **kwargs):
        context = super(AdministratorAccountingView, self).get_context_data(**kwargs)
        
        context['project_names'] = [p.title for p in Project.objects.all()]
        context['admin_repayments'] = AdminRepayment.objects.repayments()
        context['admin_reinvestments'] = AdminReinvestment.objects.reinvestments()
        context['donations'] = Payment.objects.donations()
        context['jsonurl'] = unicode(str(reverse('administrator:accountingJSON')))

        return context

class AccountingJSONView(View):
    
    beginning_of_time = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')

    start_date = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.now()
    project_filter = Project.objects.all()

    def calculateCashBalanceFromStart(self):
        # compare the beginning of time to the start_date
        # TODO : DO THIS METHOD
        pass

    def updateFilterVariables(self, keys):
        try:
            if 'start_date' in keys:
                self.start_date = datetime.datetime.strptime(request['start_date'], '%Y-%m-%d')
            elif 'end_date' in keys:
                self.end_date = datetime.datetime.strptime(request['end_date'], '%Y-%m-%d')
            elif 'project_filter' in keys:
                if (request['project'] == 'all'):
                    self.project_filter = Project.objects.all()
                else:
                    self.project_filter = Project.objects.filter(title=request['project']) 
        except ValueError:
            pass

    def setUpFilteredDict(self):
        filtered_dict = {'cash_in': {'repayments': {}, 'adjustments': {}, 'donations': {}}, 'cash_out': {'reinvestments': {}, 'adjustments': {}}}
        
        filtered_dict['date_info'] = {}
        date_info = filtered_dict['date_info']
        date_info['start_date'] = self.start_date.strftime('%Y-%m-%d')
        date_info['end_date'] = self.end_date.strftime('%Y-%m-%d')
        date_info['date_list'] = []
        filtered_dict['current_cash_balance'] = self.calculateCashBalanceFromStart()
        filtered_dict['project_names'] = []
        project_names = filtered_dict['project_names']
        for proj in self.project_filter:
            project_names.append(proj.title)

        return filtered_dict

    def dispatch(self, request, *args, **kwargs):
        request = request.GET
        keys = request.keys()
        
        #THESE ARE DUMMY VARIABLES - USE THE REVOLV EARNINGS MODEL INSTEAD
        payment_service_fee_rate = 0.01
        revolv_earnings_rate = 0.07

        self.updateFilterVariables(keys)

        filtered_dict = self.setUpFilteredDict()      
        date_info = filtered_dict['date_info']
        date_list = date_info['date_list']

        cash_in_repayment = filtered_dict['cash_in']['repayments']
        cash_in_donation = filtered_dict['cash_in']['donations']
        cash_in_adjustment = filtered_dict['cash_in']['adjustments']
        cash_out_reinvestment = filtered_dict['cash_out']['reinvestments']
        cash_out_adjustment = filtered_dict['cash_out']['adjustments']

        temp_start_date = self.start_date
        new_month = (self.start_date.month)%12 + 1
        if new_month==1:
            new_year = self.start_date.year + 1
            temp_end_date = self.start_date.replace(month=new_month, year=new_year)
        else:
            temp_end_date = self.start_date.replace(month=new_month)

        while temp_start_date < self.end_date:
            if (self.end_date < temp_end_date):
                temp_end_date = self.end_date

            date_list.append(temp_start_date.strftime('%Y-%m-%d'))

            date = temp_start_date.strftime('%Y-%m-%d')
            cash_in_repayment[date] = {}
            cash_in_donation[date] = {}
            cash_in_adjustment[date] = {}
            cash_out_reinvestment[date] = {}
            cash_out_adjustment[date] = {}

            cash_in_repayment_date = cash_in_repayment[date]
            cash_in_donation_date = cash_in_donation[date]
            cash_in_adjustment_date = cash_in_adjustment[date]
            cash_out_reinvestment_date = cash_out_reinvestment[date]
            cash_out_adjustment_date = cash_out_adjustment[date]

            current_dict = cash_in_adjustment_date
            total = sum([adjustment for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_in')])
            current_dict['total'] = total

            current_dict['transactions'] = {}
            current_dict = current_dict['transactions']
            for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_in'):
                current_dict[adjustment.name] = str(amount)

            current_dict = cash_out_adjustment_date
            total = sum([adjustment for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_out')])
            current_dict['total'] = total

            current_dict['transactions'] = {}
            current_dict = current_dict['transactions']
            for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_out'):
                current_dict[adjustment.name] = str(amount)

            for proj in self.project_filter:
                
                cash_in_repayment_date[proj.title] = {}
                cash_in_donation_date[proj.title] = {}
                cash_out_reinvestment_date[proj.title] = {}

                current_dict = cash_in_repayment_date[proj.title]
                total = sum([repayment.amount for repayment in AdminRepayment.objects.repayments(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
                current_dict['total'] = total
                current_dict['revolv_earnings'] = total * revolv_earnings_rate
                current_dict['retained_ROI'] = total * (1 - revolv_earnings_rate)

                current_dict = cash_in_donation_date[proj.title] 
                total =  sum([donation.amount for donation in Payment.objects.donations(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
                current_dict['total'] = total
                current_dict['payment_service_fees'] = total * payment_service_fee_rate
                current_dict['retained_donations'] = total * (1 - payment_service_fee_rate)

                current_dict = cash_out_reinvestment_date[proj.title]
                total = sum([reinvestment.amount for reinvestment in AdminReinvestment.objects.reinvestments(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
                current_dict['total'] = total
            
            temp_start_date = temp_end_date
            new_month = (temp_end_date.month)%12 + 1
            if new_month==1:
                new_year = temp_end_date.year + 1
                temp_end_date = temp_end_date.replace(month=new_month, year=new_year)
            else:
                temp_end_date = temp_end_date.replace(month=new_month)

        return JsonResponse(filtered_dict)

class AdministratorAddAdjustmentView(CreateView):
    
    model = AdminAdjustment
    template_name = 'administrator/adjustment.html'

    def get_success_url(self):
        return reverse('administrator:accounting')

    def get_form_kwargs(self):
        kwargs = super(AdministratorAddAdjustmentView, self).get_form_kwargs()
        self.form = AdjustmentForm(initial={'admin': RevolvUserProfile.objects.filter(user=self.request.user)[0]})
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
