from copy import deepcopy
from datetime import date

from django import forms
from revolv.payments.lib.instruments import (CreditCard,
                                             PayPalCreditCardInstrument)
from revolv.payments.services import PaymentService


class DonationForm(forms.Form):
    amount = forms.DecimalField()


class CreditCardDonationForm(DonationForm):
    """
        Form for creating a donation from a credit card.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()

    cardtype_choices = [
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('discover', 'Discover'),
        ('amex', 'American Express')
    ]
    type = forms.ChoiceField(choices=cardtype_choices)

    month_choices = [(n, None) for n in range(1, 12 + 1)]
    expire_month = forms.ChoiceField(choices=month_choices)

    this_year = date.today().year
    year_choices = [(n, None) for n in range(this_year, this_year + 10 + 1)]
    expire_year = forms.ChoiceField(choices=year_choices)

    cvv2 = forms.IntegerField()
    number = forms.IntegerField()

    def process_payment(self, project, user):
        """
        Process the payment with given the credit card information.

        :project: revolv.project.models.Project
        :user: the User making the payment
        :return:
        """
        if not self.is_valid():
            raise Exception('Cannot process invalid form')

        # Remove the amount field for the tuple
        cc_dict = deepcopy(self.cleaned_data)
        del cc_dict['amount']

        credit_card = CreditCard(**cc_dict)

        instrument = PayPalCreditCardInstrument(credit_card)

        # TODO: error handling
        # Make the payment
        payment = PaymentService.create_payment(
            user.revolvuserprofile,
            user.revolvuserprofile,
            self.cleaned_data.get('amount'),
            project,
            instrument
        )

        # Add RevolvUserProfile to donors field of Project
        project.donors.add(user.revolvuserprofile)

        return payment
