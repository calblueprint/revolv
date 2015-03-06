import datetime

import factory
from revolv.payments.models import Payment, PaymentInstrumentType


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.models.RevolvUserProfileFactory")
    entrant = factory.SubFactory("revolv.base.models.RevolvUserProfileFactory")
    amount = 20.00
    project = factory.SubFactory("revolv.project.models.ProjectFactory")
    payment_instrument_type = PaymentInstrumentType.objects.get_paypal()
    created_at = datetime.datetime.now()


class PaymentFactories(object):
    base = PaymentFactory
