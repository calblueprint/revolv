from copy import deepcopy

from django import forms
from revolv.payments.lib.instruments import (CreditCard,
                                             PayPalCreditCardInstrument)
from revolv.payments.services import DonationService, PaymentService


class DonationForm(forms.Form):
    amount = forms.DecimalField()


class CreditCardDonationForm(DonationForm):
    """
        Form for creating a donation from a credit card.
    """
    first_name = forms.CharField()
    last_name = forms.CharField()

    # Note: this will be parsed on the frontend
    type = forms.CharField()

    expire_month = forms.CharField()
    expire_year = forms.CharField()
    cvv2 = forms.CharField()
    number = forms.CharField()

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
        payment_transaction = PaymentService.create_payment(
            user,
            self.cleaned_data.get('amount'),
            instrument
        )

        # Link the payment to a donation
        donation = DonationService.link_donation(
            project,
            payment_transaction
        )
        return donation
