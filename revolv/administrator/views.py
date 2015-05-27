import csv
import json
import datetime

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
    """View of the administrator accounting page.
    """
    template_name = 'administrator/accounting.html'

    def clean_project_name(self, name):
        name = name.replace(' ', '-').replace(';', 'sm').replace(':', 'co').replace("'", 'ap').replace('!', 'ex')
        return name

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
            clean_project_names[self.clean_project_name(p)] = p

        return context

class AccountingJSONView(View):
    """
    A view that returns a JsonResponse of all relevant accounting data.
    This is queried by an AJAX request when creating the Accounting page.

    The data is roughly structured as shown below:
    data = {
        'cash_in': {},
        'cash_out': {},
        'date_info': {},
        'project_names': [],
        'cash_balances': {},
        'clean_project_names': [],
        }
    """

    start_date = datetime.datetime.strptime('2015-01-01', '%Y-%m-%d')
    end_date = datetime.datetime.now()
    project_filter = Project.objects.all()

    project_dict = {}


    """
    A helper function that calculates the initial cash balance from the
    beginning of time to self.start_date

    :return:
        Returns a number that represents initial cash balance.
    """
    def calculateCashBalanceFromStart(self):
        # THESE ARE DUMMY VARIABLES - USE THE REVOLV EARNINGS MODEL INSTEAD
        payment_service_fee_rate = 0.01
        revolv_earnings_rate = 0.07
        allDonations = sum([payment.amount for payment in Payment.objects.donations(end_date=self.start_date)])
        allReinvestments = sum([payment.amount for payment in AdminReinvestment.objects.reinvestments(end_date=self.start_date)])
        allRepayments = sum([payment.amount for payment in AdminRepayment.objects.repayments(end_date=self.start_date)])
        cashInAdjustments = sum([payment.amount for payment in AdminAdjustment.objects.adjustments(end_date=self.start_date, cash_type='cash_in')])
        cashOutAdjustments = sum([payment.amount for payment in AdminAdjustment.objects.adjustments(end_date=self.start_date, cash_type='cash_out')])

        cash_in = (allDonations * (1 - payment_service_fee_rate)) + (allRepayments * (1 - revolv_earnings_rate)) + cashInAdjustments
        cash_out  = cashOutAdjustments + allReinvestments
        net = cash_in - cash_out
        return net
    
    """
    A helper function that cleans a project name to make it JQuery 
    friendly for use in the Accounting page.

    :args:
        name: A string to be cleaned

    :return:
        Returns a cleaned up version of name.
    """
    def clean_project_name(self, name):
        name = name.replace(' ', '-').replace(';', 'sm').replace(':', 'co').replace("'", 'ap').replace('!', 'ex')
        return name
    
    def make_project_dict(self):
        self.project_dict = {}
        for proj in Project.objects.all():
            name = proj.title
            self.project_dict[self.clean_project_name(name)] = name
    
    """
    Updates class variables such as start_date, end_date, and project_filter
    based on the keys passed in.

    :args:
        keys: The request passed in to the AccountingJSONView
    """
    def updateFilterVariables(self, keys):
        self.make_project_dict()

        try:
            if 'start_date' in keys:
                self.start_date = datetime.datetime.strptime(keys['start_date'], '%Y-%m-%d')
            elif 'end_date' in keys:
                self.end_date = datetime.datetime.strptime(keys['end_date'], '%Y-%m-%d')
            elif 'project_choice' in keys:
                if keys['project_choice'] == 'all':
                    self.project_filter = Project.objects.all()
                else:
                    real_name = self.project_dict[keys['project_choice']]
                    self.project_filter = Project.objects.filter(title=real_name)
        except ValueError:
            pass
    
    """
    Sets up the basics of a JSON serializable dictionary.
    This sets up:
    1. cash_in and its various components (repayments, adjustments, donations)
    2. cash_out and its various components (reinvestments, adjustments)
    3. date_info and its various components (start_date, end_date, date_list)
    4. cash_balances
    5. project_names
    6. clean_project_names
    7. cash_in/out_adjustment_names, which is a list of all the names of adjustments created

    :return:
        Returns a properly set up dictionary.
    """
    def setUpFilteredDict(self):
        filtered_dict = {'cash_in': {'repayments': {}, 'adjustments': {}, 'donations': {}}, 'cash_out': {'reinvestments': {}, 'adjustments': {}}}
        
        filtered_dict['date_info'] = {}
        filtered_dict['cash_balances'] = {}
        date_info = filtered_dict['date_info']
        date_info['start_date'] = self.start_date.strftime('%Y-%m-%d')
        date_info['end_date'] = self.end_date.strftime('%Y-%m-%d')
        date_info['date_list'] = []
        filtered_dict['project_names'] = []
        filtered_dict['clean_project_names'] = []
        clean_project_names = filtered_dict['clean_project_names']
        project_names = filtered_dict['project_names']
        for proj in self.project_filter:
            if (self.hasPayments(proj)):
                project_names.append(proj.title)
                clean_project_names.append(self.clean_project_name(proj.title))

        filtered_dict['cash_in_adjustment_names'] = list(set([adj.name for adj in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_in')]))
        filtered_dict['cash_out_adjustment_names'] = list(set([adj.name for adj in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_out')]))

        return filtered_dict
    
    """
    Checks whether a project has any associated donations, reinvestments, or repayments.

    :args:
        project: The project to check.

    :return:
        A boolean of whether the project has associated payment objects.
    """
    def hasPayments(self, project):
        donations = len(Payment.objects.donations(project=project, start_date=self.start_date, end_date=self.end_date))
        reinvestments = len(AdminReinvestment.objects.reinvestments(project=project, start_date=self.start_date, end_date=self.end_date))
        repayments = len(AdminRepayment.objects.repayments(project=project, start_date=self.start_date, end_date=self.end_date))

        return (donations + reinvestments + repayments) != 0

    """
    A helper function that returns a date one month ahead of the date
    passed in.

    :return:
        A Python datetime.datetime object with a time value one month ahead of date.
    """
    def moveOneMonthForward(self, date):
        new_month = (date.month)%12 + 1
        if new_month==1:
            new_year = date.year + 1
            new_date = date.replace(month=new_month, year=new_year)
        else:
            new_date = date.replace(month=new_month)
        return new_date

    """
    Sets up subdictionaries of each Payment object model for a certain date.

    :args:
        filtered_dict: The JSON serializable dictionary to be modified.
        date: The current date period we are iterating over.
    """
    def makePaymentTypeKeys(self, filtered_dict, date):
        filtered_dict['cash_in']['repayments'][date] = {}
        filtered_dict['cash_in']['donations'][date] = {}
        filtered_dict['cash_in']['adjustments'][date] = {}
        filtered_dict['cash_out']['adjustments'][date] = {}
        filtered_dict['cash_out']['reinvestments'][date] = {}
        filtered_dict['cash_balances'][date] = {}
    
    """
    Sets up subdictionaries of each Payment object model for a certain date and project.

    :args:
        filtered_dict: The JSON serializable dictionary to be modified.
        date: The current date period we are iterating over.
        title: The title of the project.
    """
    def makeProjectKeys(self, filtered_dict, date, title):
        filtered_dict['cash_in']['repayments'][date][title] = {}
        filtered_dict['cash_in']['donations'][date][title] = {}
        filtered_dict['cash_out']['reinvestments'][date][title] = {}
    
    """
    For a specific date period, adds beginning cash balance, change
    in cash balance, and final cash balance to the JSON serializable
    dictionary.

    :args:
        cash: A subdictionary of the JSON serializable dictionary filtered_dict.
        cash_balance: The cash balance at the beginning of this period.
        net_cash_in: Net inflow of cash during this period.
        net_cash_out: Net outflow of cash during this period.
    """
    def setCashBalances(self, cash, cash_balance, net_cash_in, net_cash_out):
        cash['beginning_cash_balance'] = cash_balance
        cash['change_in_cash'] = net_cash_in - net_cash_out
        cash['final_cash_balance'] = cash_balance + net_cash_in - net_cash_out
        cash['net_cash_in'] = net_cash_in
        cash['net_cash_out'] = net_cash_out
    
    """
    Creates and fills in the 'adjustment' subdictionary of 'cash_in' and 'cash_out'
    within the JSON serializable dictionary.

    :args:
        cash: A subdictionary of the JSON serializable dictionary filtered_dict.
        cash_balance: The cash balance at the beginning of this period.
        net_cash_in: Net inflow of cash during this period.
        net_cash_out: Net outflow of cash during this period.
    """
    def setTimePeriodAdjustments(self, filtered_dict, date, temp_start_date, temp_end_date):
        filtered_dict['cash_in']['adjustments'][date]['transactions'] = {}
        current_dict = filtered_dict['cash_in']['adjustments'][date]['transactions']
        for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_in'):
            if adjustment.name in current_dict:
                current_dict[adjustment.name] += adjustment.amount
            else:
                current_dict[adjustment.name] = adjustment.amount
        
        current_dict = filtered_dict['cash_in']['adjustments'][date]
        total = sum([adjustment.amount for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_in')])
        current_dict['total'] = total

        filtered_dict['cash_out']['adjustments'][date]['transactions'] = {}
        current_dict = filtered_dict['cash_out']['adjustments'][date]['transactions']
        for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_out'):
            if adjustment.name in current_dict:
                current_dict[adjustment.name] += adjustment.amount
            else:
                current_dict[adjustment.name] = adjustment.amount

        current_dict = filtered_dict['cash_out']['adjustments'][date]
        total = sum([adjustment.amount for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type='cash_out')])
        current_dict['total'] = total
    
    """
    Creates and fills in the 'repayments' subdictionary of 'cash_in' and 'cash_out'
    within the JSON serializable dictionary for a certain time period and project.

    :args:
        filtered_dict: The JSON serializable dictionary.
        date: A string represenation of temp_start_date.
        proj: The project of interest.
        temp_start_date: The start date of this time period.
        temp_end_date: The end date of this time period.
        revolv_earnings_rate: A float from 0-1 representing what percentage of repayments RE-volv takes as earnings.
    """
    def setRepaymentTableValues(self, filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate):
        current_dict = filtered_dict['cash_in']['repayments'][date][proj.title]
        total = sum([repayment.amount for repayment in AdminRepayment.objects.repayments(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
        current_dict['total'] = total
        current_dict['revolv_earnings'] = total * revolv_earnings_rate
        current_dict['retained_ROI'] = total * (1 - revolv_earnings_rate)
    
    """
    Creates and fills in the 'donations' subdictionary of 'cash_in' and 'cash_out'
    within the JSON serializable dictionary for a certain time period and project.

    :args:
        filtered_dict: The JSON serializable dictionary.
        date: A string represenation of temp_start_date.
        proj: The project of interest.
        temp_start_date: The start date of this time period.
        temp_end_date: The end date of this time period.
        payment_service_fee_rate: A float from 0-1 representing what percentage of donations that are taken by payment service fees.
    """
    def setDonationTableValues(self, filtered_dict, date, proj, temp_start_date, temp_end_date, payment_service_fee_rate):
        current_dict['filtered_dict']['donations'][date][proj.title]
        total = sum([donation.amount for donation in Payment.objects.donations(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
        current_dict['total'] = total
        current_dict['payment_service_fees'] = total * payment_service_fee_rate
        current_dict['retained_donations'] = total * (1 - payment_service_fee_rate)
    
    """
    Creates and fills in the 'reinvestments' subdictionary of 'cash_in' and 'cash_out'
    within the JSON serializable dictionary for a certain time period and project.

    :args:
        filtered_dict: The JSON serializable dictionary.
        date: A string represenation of temp_start_date.
        proj: The project of interest.
        temp_start_date: The start date of this time period.
        temp_end_date: The end date of this time period.
    """
    def setReinvestmentTableValues(self, filtered_dict, date, proj, temp_start_date, temp_end_date):
        current_dict['cash_out']['reinvestments'][date][proj.title]
        total = sum([reinvestment.amount for reinvestment in AdminReinvestment.objects.reinvestments(project=proj, start_date=temp_start_date, end_date=temp_end_date)])
        current_dict['total'] = total

    """
    Creates and fills in the 'repayments', 'reinvestments', and 'donations' subdictionary of 'cash_in' and 'cash_out'
    within the JSON serializable dictionary for a certain time period and project.

    :args:
        filtered_dict: The JSON serializable dictionary.
        date: A string represenation of temp_start_date.
        proj: The project of interest.
        temp_start_date: The start date of this time period.
        temp_end_date: The end date of this time period.
        revolv_earnings_rate: A float from 0-1 representing what percentage of repayments RE-volv takes as earnings.
        payment_service_fee_rate: A float from 0-1 representing what percentage of donations that are taken by payment service fees.
    """
    def setAlTableValues(self, filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate, payment_service_fee_rate):
        self.setRepaymentTableValues(filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate)
        self.setDonationTableValues(filtered_dict, date, proj, temp_start_date, temp_end_date, payment_service_fee_rate)
        self.setReinvestmentTableValues(filtered_dict, date, proj, temp_start_date, temp_end_date)

    """
    Creates and returns a JsonResponse.
    """
    def dispatch(self, request, *args, **kwargs):
        request = request.GET
        keys = request.keys()
        
        # THESE ARE DUMMY VARIABLES - USE THE REVOLV EARNINGS MODEL INSTEAD
        payment_service_fee_rate = 0.01
        revolv_earnings_rate = 0.07

        self.updateFilterVariables(request)

        filtered_dict = self.setUpFilteredDict()      
        date_info = filtered_dict['date_info']
        date_list = date_info['date_list']

        cash_in_repayment = filtered_dict['cash_in']['repayments']
        cash_in_donation = filtered_dict['cash_in']['donations']
        cash_in_adjustment = filtered_dict['cash_in']['adjustments']
        cash_out_reinvestment = filtered_dict['cash_out']['reinvestments']
        cash_out_adjustment = filtered_dict['cash_out']['adjustments']

        temp_start_date = self.start_date
        temp_end_date = self.moveOneMonthForward(temp_start_date)

        cash_balance = self.calculateCashBalanceFromStart()
        filtered_project_filter = [proj for proj in self.project_filter if self.hasPayments(proj)]
        
        while temp_start_date < self.end_date:
            net_cash_in = 0
            net_cash_out = 0

            if (self.end_date < temp_end_date):
                temp_end_date = self.end_date

            date_list.append(temp_start_date.strftime('%Y-%m-%d'))
            date = temp_start_date.strftime('%Y-%m-%d')        
            self.makePaymentTypeKeys(filtered_dict, date)

            cash_in_repayment_date = cash_in_repayment[date]
            cash_in_donation_date = cash_in_donation[date]
            cash_in_adjustment_date = cash_in_adjustment[date]
            cash_out_reinvestment_date = cash_out_reinvestment[date]
            cash_out_adjustment_date = cash_out_adjustment[date]
            cash = filtered_dict['cash_balances'][date]

            self.setTimePeriodAdjustments(filtered_dict, date, temp_start_date, temp_end_date)
            net_cash_in += cash_in_adjustment_date['total']
            net_cash_out += cash_out_adjustment_date['total']

            for proj in filtered_project_filter:
                self.makeProjectKeys(filtered_dict, date, title)
                self.setAllTableValues(filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate, payment_service_fee_rate)
                
                net_cash_in += cash_in_repayment_date[proj.title]['retained_ROI']
                net_cash_in += cash_in_donation_date[proj.title]['retained_donations']
                net_cash_out += cash_out_reinvestment_date[proj.title]['total']
            
            self.setCashBalances(cash, cash_balance, net_cash_in, net_cash_out)
            cash_balance += net_cash_in - net_cash_out

            temp_start_date = temp_end_date
            temp_end_date = self.moveOneMonthForward(temp_end_date)
        
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
