import datetime
import urllib

from django.db.models import Sum
from revolv.payments.models import Payment, AdminReinvestment, AdminRepayment, AdminAdjustment
from revolv.project.models import Project

class NotEnoughFundingException(Exception):
    pass


class ProjectNotCompleteException(Exception):
    pass

class AccountingAggregator():
    
    """
    An aggregator class that does much of the computation for the AdministratorAccountingView
    view in revolv.administrator.views.
    """

    def __init__(self, start_date=None, end_date=None, project_filter=None, revolv_earnings_rate=0, payment_service_fee_rate=0):
        # to prevent uneccessary operations
        if start_date:
            self.start_date = start_date
            self.end_date = end_date
            self.project_filter = project_filter
            self.revolv_earnings_rate = revolv_earnings_rate
            self.payment_service_fee_rate = payment_service_fee_rate
            self.allProjects = Project.objects.all()

    def calculate_cash_balance_from_start(self):
        """
        A helper function that calculates the initial cash balance from the
        beginning of time to self.start_date

        :return:
            Returns a number that represents initial cash balance.
        """
        all_donations = Payment.objects.donations(end_date=self.start_date).aggregate(Sum('amount'))['amount__sum']
        all_reinvestments = AdminReinvestment.objects.reinvestments(end_date=self.start_date).aggregate(Sum('amount'))['amount__sum']
        all_repayments = AdminRepayment.objects.repayments(end_date=self.start_date).aggregate(Sum('amount'))['amount__sum']
        cash_in_adjustments = AdminAdjustment.objects.adjustments(end_date=self.start_date, cash_type='cash_in').aggregate(Sum('amount'))['amount__sum']
        cash_out_adjustments = AdminAdjustment.objects.adjustments(end_date=self.start_date, cash_type='cash_out').aggregate(Sum('amount'))['amount__sum']

        if not all_donations:
            all_donations = 0
        if not all_reinvestments:
            all_reinvestments = 0
        if not all_repayments:
            all_repayments = 0
        if not cash_in_adjustments:
            cash_in_adjustments = 0
        if not cash_out_adjustments:
            cash_out_adjustments = 0

        cash_in = (all_donations * (1 - self.payment_service_fee_rate)) + (all_repayments * (1 - self.revolv_earnings_rate)) + cash_in_adjustments
        cash_out  = cash_out_adjustments + all_reinvestments
        net = cash_in - cash_out
        return net

    def clean_project_name(self, name):
        """
        A helper function that cleans a project name to make it JQuery 
        friendly for use in the Accounting page.

        :args:
            name: A string to be cleaned

        :return:
            Returns a cleaned up version of name.
        """
        new_name = ""
        for c in name:
            value = ord(c)
            if value < 65 or value > 122:
                new_name += 'z'
            else:
                new_name += c
        return new_name

    def has_payments(self, project):
        """
        Checks whether a project has any associated donations, reinvestments, or repayments.

        :args:
            project: The project to check.

        :return:
            A boolean of whether the project has associated payment objects.
        """
        donations = Payment.objects.donations(project=project, start_date=self.start_date, end_date=self.end_date).count()
        reinvestments = AdminReinvestment.objects.reinvestments(project=project, start_date=self.start_date, end_date=self.end_date).count()
        repayments = AdminRepayment.objects.repayments(project=project, start_date=self.start_date, end_date=self.end_date).count()

        return (donations + reinvestments + repayments) != 0

    def move_one_month_forward(self, date):
        """
        A helper function that returns a date one month ahead of the date
        passed in.

        :return:
            A Python datetime.datetime object with a time value one month ahead of date.
        """
        new_month = (date.month)%12 + 1
        if new_month==1:
            new_year = date.year + 1
            new_date = date.replace(month=new_month, year=new_year)
        else:
            new_date = date.replace(month=new_month)
        return new_date

    def set_up_filtered_dict(self):
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
        filtered_dict = {}
        filtered_dict['cash_in'] = {'repayments': {}, 'adjustments': {}, 'donations': {}}
        filtered_dict['cash_out'] = {'reinvestments': {}, 'adjustments': {}}  
        filtered_dict['date_info'] = {}
        filtered_dict['cash_balances'] = {}
        date_info = filtered_dict['date_info']
        date_info['start_date'] = self.start_date.strftime('%Y-%m-%d')
        date_info['end_date'] = self.end_date.strftime('%Y-%m-%d')
        date_info['date_list'] = []
        filtered_dict['project_names'] = []
        project_names = filtered_dict['project_names']
        for proj in self.project_filter:
            if (self.has_payments(proj)):
                project_names.append(proj.title)

        filtered_dict['cash_in_adjustment_names'] = [adj.name for adj in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_in').distinct()]
        filtered_dict['cash_out_adjustment_names'] = [adj.name for adj in AdminAdjustment.objects.adjustments(start_date=self.start_date, end_date=self.end_date, cash_type='cash_out').distinct()]

        return filtered_dict

    def make_payment_type_keys(self, filtered_dict, date):
        """
        Sets up subdictionaries of each Payment object model for a certain date.

        :args:
            filtered_dict: The JSON serializable dictionary to be modified.
            date: The current date period we are iterating over.
        """
        paths = [['cash_in', 'repayments'], ['cash_in', 'donations'], ['cash_in', 'adjustments'], ['cash_out', 'adjustments'], ['cash_out', 'reinvestments']]
        for path in paths:
            filtered_dict[path[0]][path[1]][date] = {}
        
        filtered_dict['cash_balances'][date] = {}
    
    def make_project_keys(self, filtered_dict, date, title):
        """
        Sets up subdictionaries of each Payment object model for a certain date and project.

        :args:
            filtered_dict: The JSON serializable dictionary to be modified.
            date: The current date period we are iterating over.
            title: The title of the project.
        """
        filtered_dict['cash_in']['repayments'][date][title] = {}
        filtered_dict['cash_in']['donations'][date][title] = {}
        filtered_dict['cash_out']['reinvestments'][date][title] = {}
    
    def set_cash_balances(self, cash, cash_balance, net_cash_in, net_cash_out):
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
        cash['beginning_cash_balance'] = cash_balance
        cash['change_in_cash'] = net_cash_in - net_cash_out
        cash['final_cash_balance'] = cash_balance + net_cash_in - net_cash_out
        cash['net_cash_in'] = net_cash_in
        cash['net_cash_out'] = net_cash_out
    
    def set_time_period_adjustments(self, filtered_dict, date, temp_start_date, temp_end_date):
        """
        Creates and fills in the 'adjustment' subdictionary of 'cash_in' and 'cash_out'
        within the JSON serializable dictionary.
        The dictionary structure is as follows:
        date: {
            'total': 5,
            'transactions': {
                transaction_name: 2,
                transaction_name: 3,
            },
        }

        :args:
            cash: A subdictionary of the JSON serializable dictionary filtered_dict.
            cash_balance: The cash balance at the beginning of this period.
            net_cash_in: Net inflow of cash during this period.
            net_cash_out: Net outflow of cash during this period.
        """
        for in_or_out in ['cash_in', 'cash_out']:
            # creates the 'transactions' subdictionary
            filtered_dict[in_or_out]['adjustments'][date]['transactions'] = {}
            current_dict = filtered_dict[in_or_out]['adjustments'][date]['transactions']
            # adds each transaction to the 'transactions' subdictionary
            for adjustment in AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type=in_or_out):
                if adjustment.name in current_dict:
                    current_dict[adjustment.name] += adjustment.amount
                else:
                    current_dict[adjustment.name] = adjustment.amount
            # switches subdictionaries and fills in the 'total' value
            current_dict = filtered_dict[in_or_out]['adjustments'][date]
            total = AdminAdjustment.objects.adjustments(start_date=temp_start_date, end_date=temp_end_date, cash_type=in_or_out).aggregate(Sum('amount'))['amount__sum']
            if not total:
                total = 0
            current_dict['total'] = total
    
    def set_repayment_table_values(self, filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate):
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
        current_dict = filtered_dict['cash_in']['repayments'][date][proj.title]
        total = AdminRepayment.objects.repayments(project=proj, start_date=temp_start_date, end_date=temp_end_date).aggregate(Sum('amount'))['amount__sum']
        if not total:
            total = 0
        current_dict['total'] = total
        current_dict['revolv_earnings'] = total * revolv_earnings_rate
        current_dict['retained_ROI'] = total * (1 - revolv_earnings_rate)
    
    def set_donation_table_values(self, filtered_dict, date, proj, temp_start_date, temp_end_date, payment_service_fee_rate):
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
        current_dict['filtered_dict']['donations'][date][proj.title]
        total = Payment.objects.donations(project=proj, start_date=temp_start_date, end_date=temp_end_date).aggregate(Sum('amount'))['amount__sum']
        if not total:
            total = 0
        current_dict['total'] = total
        current_dict['payment_service_fees'] = total * payment_service_fee_rate
        current_dict['retained_donations'] = total * (1 - payment_service_fee_rate)
    
    def set_reinvestment_table_values(self, filtered_dict, date, proj, temp_start_date, temp_end_date):
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
        current_dict['cash_out']['reinvestments'][date][proj.title]
        total = AdminReinvestment.objects.reinvestments(project=proj, start_date=temp_start_date, end_date=temp_end_date).aggregate(Sum('amount'))['amount__sum']
        if not total:
            total = 0
        current_dict['total'] = total

    def set_all_table_values(self, filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate, payment_service_fee_rate):
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
        self.set_repayment_table_values(filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate)
        self.set_donation_table_values(filtered_dict, date, proj, temp_start_date, temp_end_date, payment_service_fee_rate)
        self.set_reinvestment_table_values(filtered_dict, date, proj, temp_start_date, temp_end_date)

    def aggregate(self):
        """
        PUT DOCUMENTATION FOR THIS FUNCTION IN HERE
        """
        # sets up the basic filtered dictionary
        filtered_dict = self.set_up_filtered_dict()
        
        # temp_start_date and temp_end_date are the boundaries for each time period
        # cash_balance is the amount of cash available at the start of the period
        # filtered_project_filter is the projects included that have transactions during this overall time period
        temp_start_date = self.start_date
        temp_end_date = self.move_one_month_forward(temp_start_date)
        cash_balance = self.calculate_cash_balance_from_start()
        filtered_project_filter = [proj for proj in self.project_filter if self.has_payments(proj)]
        
        while temp_start_date < self.end_date:
            net_cash_in = 0
            net_cash_out = 0

            if (self.end_date < temp_end_date):
                temp_end_date = self.end_date

            # creates subdictionaries for this specific date and for adjustments within that date
            filtered_dict['date_info']['date_list'].append(temp_start_date.strftime('%Y-%m-%d'))
            date = temp_start_date.strftime('%Y-%m-%d')        
            self.make_payment_type_keys(filtered_dict, date)
            self.set_time_period_adjustments(filtered_dict, date, temp_start_date, temp_end_date)
            net_cash_in += filtered_dict['cash_in']['adjustments'][date]['total']
            net_cash_out += filtered_dict['cash_out']['adjustments'][date]['total']

            # creates project subdictionaries for this each project and inserts their respective transactions
            for proj in filtered_project_filter:
                self.make_project_keys(filtered_dict, date, title)
                self.set_all_table_values(filtered_dict, date, proj, temp_start_date, temp_end_date, revolv_earnings_rate, payment_service_fee_rate)
                
                net_cash_in += filtered_dict['cash_in']['repayments'][date][proj.title]['retained_ROI']
                net_cash_in += filtered_dict['cash_in']['donations'][date][proj.title]['retained_donations']
                net_cash_out += filtered_dict['cash_out']['reinvestments'][date][proj.title]['total']
            
            # fills in the inital cash balance, change in cash, and the final cash balance for this time period
            cash = filtered_dict['cash_balances'][date]
            self.set_cash_balances(cash, cash_balance, net_cash_in, net_cash_out)
            cash_balance += net_cash_in - net_cash_out

            # updates the time variables for the next iteration
            temp_start_date = temp_end_date
            temp_end_date = self.move_one_month_forward(temp_end_date)

        return filtered_dict

