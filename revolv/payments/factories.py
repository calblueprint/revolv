import datetime

import factory
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, Repayment)


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    entrant = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_type = PaymentType.objects.get_paypal()
    created_at = datetime.datetime.now()


example_user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")


class DonationPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = example_user
    entrant = example_user
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_type = PaymentType.objects.get_paypal()
    created_at = datetime.datetime.now()


class PaymentFactories(object):
    base = PaymentFactory
    donation = DonationPaymentFactory


class AdminRepaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdminRepayment

    admin = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    amount = 20.00
    created_at = datetime.datetime.now()


class AdminRepaymentFactories(object):
    base = AdminRepaymentFactory


class AdminReinvestmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdminReinvestment

    admin = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    amount = 20.00
    created_at = datetime.datetime.now()


class AdminReinvestmentFactories(object):
    base = AdminReinvestmentFactory


class RepaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repayment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    admin_repayment = factory.SubFactory("revolv.project.factories.AdminRepaymentFactories")
    amount = 20.00
    created_at = datetime.datetime.now()


class RepaymentFactories(object):
    base = RepaymentFactory
