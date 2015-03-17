from django.db.models import Sum, signals
from django.dispatch import receiver
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, Repayment)
from revolv.payments.utils import (NotEnoughFundingException,
                                   ProjectNotCompleteException)


@receiver(signals.pre_init, sender=AdminRepayment)
def pre_init_admin_repayment(**kwargs):
    """
    Make sure that related project is indeed complete, else throw a
    ProjectNotCompleteException and to disallow instantiation of an invalid
    AdminRepayment.
    """
    init_kwargs = kwargs.get('kwargs')
    if not init_kwargs:
        raise NotEnoughFundingException()
    project = init_kwargs.get('project')
    if not project.is_completed:
        raise ProjectNotCompleteException()


@receiver(signals.post_save, sender=AdminRepayment)
def post_save_admin_repayment(**kwargs):
    """
    When an AdminRepayment is saved, a Repayment is generated for all donors to
    a project, each weighed by that donor's proportion of the contribution to
    the project.
    """
    instance = kwargs.get('instance')
    for donor in instance.project.donors.all():
        repayment = Repayment(user=donor,
                              project=instance.project,
                              admin_repayment=instance,
                              amount=(instance.project.proportion_donated(donor) * instance.amount),
                              )
        repayment.save()


@receiver(signals.pre_init, sender=AdminReinvestment)
def pre_init_admin_reinvestment(**kwargs):
    """
    Raises a NotEnoughFundingException before __init__ if there are not enough
    funds for this AdminReinvestment.
    """
    init_kwargs = kwargs.get('kwargs')
    if not init_kwargs:
        raise NotEnoughFundingException()
    invest_amount = init_kwargs.get('amount') or 0.0

    global_repay_amount = AdminRepayment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_amount = AdminReinvestment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_pool = global_repay_amount - global_reinvest_amount
    if global_reinvest_pool - invest_amount < 0.0:
        raise NotEnoughFundingException()


@receiver(signals.post_save, sender=AdminReinvestment)
def post_save_admin_reinvestment(**kwargs):
    """
    When an AdminReinvestment is saved, we pool as many donors as we need to
    fund the reinvestment, prioritizing users that have a preference for the
    Category of the project begin invested into. We only consider users that
    have a non-zero pool of investable money.

    !!! TODO: actually prioritize by Category
    """
    instance = kwargs.get('instance')
    total_left = instance.amount
    pending_reinvestors = []
    for user in RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0):
        total_left -= user.reinvest_pool
        reinvest_amount = user.reinvest_pool + min(0.0, total_left)
        pending_reinvestors.append((user, reinvest_amount))
        if total_left <= 0.0:
            break
    for (user, amount) in pending_reinvestors:
        reinvestment = Payment(user=user,
                               project=instance.project,
                               entrant=instance.admin,
                               payment_type=PaymentType.objects.get_reinvestment(),
                               admin_reinvestment=instance,
                               amount=amount
                               )
        reinvestment.save()


@receiver(signals.post_save, sender=Repayment)
def post_save_repayment(**kwargs):
    """
    When a Repayment is saved, we increment the reinvest_pool in the related
    user.
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool += instance.amount
    instance.user.save()


@receiver(signals.pre_delete, sender=Repayment)
def pre_delete_repayment(**kwargs):
    """
    Before a Repayment is deleted, we decrement the reinvest_pool in the related
    user.
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool -= instance.amount
    instance.user.save()


@receiver(signals.post_save, sender=Payment)
def post_save_payment(**kwargs):
    """
    If the payment is organic, we add this payment's user as a donor to the
    related project. If the payment is a reinvestment, we decrement the
    reinvest_pool in the related user.
    """
    instance = kwargs.get('instance')
    if instance.payment_type == PaymentType.objects.get_paypal():
        instance.project.donors.add(instance.user)
    elif instance.payment_type == PaymentType.objects.get_reinvestment():
        instance.user.reinvest_pool -= instance.amount
        instance.user.save()


@receiver(signals.pre_delete, sender=Payment)
def pre_delete_payment(**kwargs):
    """
    Before a Payment is deleted, if it is a reinvestment, we increment the
    reinvest_pool in the related user
    """
    instance = kwargs.get('instance')
    if instance.payment_type == PaymentType.objects.get_paypal():
        donation_count = instance.project.payment_set.filter(
            user=instance.user
        ).count()
        if donation_count == 1:
            instance.project.donors.remove(instance.user)
    elif instance.payment_type == PaymentType.objects.get_reinvestment():
        instance.user.reinvest_pool += instance.amount
        instance.user.save()
