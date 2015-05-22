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


class AccountingJSONView(View):
    
    start_date = datetime.datetime.strptime('2015-06-01', '%Y-%m-%d')
    end_date = datetime.datetime.now()
    project_filter = Project.objects.all()
    
    def dispatch(self, request, *args, **kwargs):

        request = request.GET
        keys = request.keys()

        #THESE ARE DUMMY VARIABLES
        payment_service_fee_rate = 0.01
        revolv_earnings_rate = 0.07

        try:
            if 'start_date' in keys:
                self.start_date = datetime.datetime.strptime(request['start_date'], '%Y-%m-%d')
            elif 'end_date' in keys:
                self.end_date = datetime.datetime.strptime(request['end_date'], '%Y-%m-%d')
            elif 'project_filter' in keys:
                self.project_filter = Project.objects.filter(title=request['project']) 
        except ValueError:
            pass

        filtered_dict = {'cash_in': {'repayments': {}, 'donations': {}, 'adjustments': {}}, 'cash_out': {'reinvestments': {}, 'adjustments': {}}}
        
        filtered_dict['date_info'] = {}
        date_info = filtered_dict['date_info']
        date_info['start_date'] = self.start_date.strftime('%Y-%m-%d')
        date_info['end_date'] = self.end_date.strftime('%Y-%m-%d')

        cash_in_repayment = filtered_dict['cash_in']['repayments']
        cash_in_donation = filtered_dict['cash_in']['donations']
        cash_in_adjustment = filtered_dict['cash_in']['adjustments']
        cash_out_reinvestment = filtered_dict['cash_out']['reinvestments']
        cash_out_adjustment = filtered_dict['cash_out']['adjustments']


        for proj in self.project_filter:
            
            cash_in_repayment[proj.title] = {}
            cash_in_donation[proj.title] = {}
            cash_in_adjustment[proj.title] = {}
            cash_out_reinvestment[proj.title] = {}
            cash_out_adjustment[proj.title] = {}


            current_dict = cash_in_donation[proj.title] 
            total =  sum([donation.amount for donation in Payment.objects.donations(project=proj, start_date=self.start_date, end_date=self.end_date)])
            #map the date to the amount IF correct range
            current_dict['total'] = total
            current_dict['payment_service_fees'] = total * payment_service_fee_rate
            current_dict['retained_donations'] = total * (1 - payment_service_fee_rate)

            current_dict = cash_in_repayment[proj.title]
            total = sum([repayment.amount for repayment in AdminRepayment.objects.repayments(project=proj, start_date=self.start_date, end_date=self.end_date)])
            current_dict['total'] = total
            current_dict['revolv_earnings'] = total * revolv_earnings_rate
            current_dict['retained_ROI'] = total * (1 - revolv_earnings_rate)

            current_dict = cash_in_adjustment[proj.title]
            total = sum([adjustment for adjustment in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_in')])
            current_dict['total'] = total

            current_dict = cash_out_adjustment[proj.title]
            total = sum([adjustment for adjustment in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_out')])
            current_dict['total'] = total

            current_dict = cash_out_reinvestment[proj.title]
            total = sum([reinvestment.amount for reinvestment in AdminReinvestment.objects.reinvestments(project=proj, start_date=self.start_date, end_date=self.end_date)])
            current_dict['total'] = total

        return JsonResponse(filtered_dict)

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
