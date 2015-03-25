import datetime

import factory
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, RepaymentFragment)
from revolv.project.models import Project


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    entrant = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    amount = 20.00
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    payment_type = PaymentType.objects.get_paypal()
    created_at = datetime.datetime.now()

# organic_user = RevolvUserProfile.factories.base.create()


class DonationPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    entrant = factory.SelfAttribute('user')
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


completed_project = Project.factories.base.create()
completed_project.complete_project()


class RepaymentFragmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RepaymentFragment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    admin_repayment = factory.SubFactory(
        "revolv.payments.factories.AdminRepaymentFactory",
        project=completed_project)
    amount = 20.00
    created_at = datetime.datetime.now()


class RepaymentFragmentFactories(object):
    base = RepaymentFragmentFactory
