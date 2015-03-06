import datetime

import factory
from revolv.payments.models import Payment, PaymentInstrumentType


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    entrant = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_instrument_type = PaymentInstrumentType.objects.get_paypal()
    created_at = datetime.datetime.now()


example_user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")


class DonationPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = example_user
    entrant = example_user
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_instrument_type = PaymentInstrumentType.objects.get_paypal()
    created_at = datetime.datetime.now()


class RepaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    entrant = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_instrument_type = PaymentInstrumentType.objects.get_repayment()
    created_at = datetime.datetime.now()


class PaymentFactories(object):
    base = PaymentFactory
    donation = DonationPaymentFactory
    repayment = RepaymentFactory
