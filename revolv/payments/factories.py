import datetime

import factory
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment, ProjectMontlyRepaymentConfig,
                                    PaymentType, RepaymentFragment, UserReinvestment)
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

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """
        Override the default _create to allow for the overriding of created_at
        See : https://github.com/rbarrois/factory_boy/issues/102
        """
        created_at = kwargs.pop('created_at', None)
        obj = super(PaymentFactory, cls)._create(target_class, *args, **kwargs)
        if created_at is not None:
            obj.created_at = created_at
            obj.save()
        return obj


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


class RepaymentFragmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RepaymentFragment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    admin_repayment = factory.SubFactory(
        "revolv.payments.factories.AdminRepaymentFactory",
        project=factory.LazyAttribute(lambda l: Project.factories.completed.create()))
    amount = 20.00
    created_at = datetime.datetime.now()


class RepaymentFragmentFactories(object):
    base = RepaymentFragmentFactory


class UserReinvestmentFactory(factory.django.DjangoModelFactory):
    """
    Factory for default UserReinvestment.
    """
    class Meta:
        model = UserReinvestment

    user = factory.SubFactory("revolv.base.factories.RevolvUserProfileFactory")
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    amount = 20.00
    created_at = datetime.datetime.now()


class ProjectMontlyRepaymentConfigFactory(factory.django.DjangoModelFactory):
    """
    Factory for default ProjectMontlyRepaymentConfig.
    """
    class Meta:
        model = ProjectMontlyRepaymentConfig
    project = factory.SubFactory("revolv.project.factories.ProjectFactory")
    year = 2015
    amount = 100.0
    repayment_type = 'SSF'
