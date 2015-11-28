from django.db.models import signals, Sum
from django.dispatch import receiver

from revolv.base.models import RevolvUserProfile
from revolv.base.utils import is_user_reinvestment_period
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, RepaymentFragment, UserReinvestment)
from revolv.payments.utils import (NotEnoughFundingException, NotInUserReinvestmentPeriodException,
                                   ProjectNotCompleteException, NotInAdminReinvestmentPeriodException,
                                   ProjectNotEligibleException)


@receiver(signals.pre_init, sender=AdminRepayment)
def pre_init_admin_repayment(**kwargs):
    """
    Make sure that related project is indeed complete, else throw a
    ProjectNotCompleteException and to disallow instantiation of an invalid
    AdminRepayment.
    """
    init_kwargs = kwargs.get('kwargs')
    # can't initialize admin_repayment without required 'project' kwarg
    if not init_kwargs or not init_kwargs.get('project'):
        raise NotEnoughFundingException()
    project = init_kwargs['project']
    if not project.is_completed:
        raise ProjectNotCompleteException()


@receiver(signals.post_save, sender=AdminRepayment)
def post_save_admin_repayment(**kwargs):
    """
    When an AdminRepayment is saved, a RepaymentFragment is generated for all
    donors to a project, each weighed by that donor's proportion of the
    contribution to the project.
    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    for donor in instance.project.donors.all():
        amount = instance.project.proportion_donated(donor) * instance.amount
        repayment = RepaymentFragment(user=donor,
                                      project=instance.project,
                                      admin_repayment=instance,
                                      amount=amount
                                      )
        # user's reinvest_pool will be incremented on save
        repayment.save()


@receiver(signals.pre_init, sender=AdminReinvestment)
def pre_init_admin_reinvestment(**kwargs):
    """
    Raises a NotEnoughFundingException before __init__ if there are not enough
    funds for this AdminReinvestment.
    """
    if is_user_reinvestment_period():
        raise NotInAdminReinvestmentPeriodException()

    init_kwargs = kwargs.get('kwargs')
    # can't initialize admin_repayment without required 'amount' kwarg
    if not init_kwargs or not init_kwargs.get('amount'):
        raise NotEnoughFundingException()
    invest_amount = init_kwargs['amount']

    global_repay_amount = AdminRepayment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_amount = AdminReinvestment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    global_user_reinvest_amount = UserReinvestment.objects.aggregate(
        Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_pool = global_repay_amount - global_reinvest_amount - global_user_reinvest_amount
    if global_reinvest_pool - invest_amount < 0.0:
        raise NotEnoughFundingException()


@receiver(signals.post_save, sender=AdminReinvestment)
def post_save_admin_reinvestment(**kwargs):
    """
    When an AdminReinvestment is saved, we pool as many donors as we need to
    fund the reinvestment, prioritizing users that have a preference for the
    Category of the project begin invested into and the by order them by thier
    last name. We only consider users that have a non-zero pool of investable money.

    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    total_left = instance.amount
    pending_reinvestors = []

    project = instance.project
    # the list of users with at least one preferred category that matches any of the
    # categories that the project is tagged with
    users_with_preferences = RevolvUserProfile.objects.filter(preferred_categories__in=project.category_set.all()).filter(reinvest_pool__gt=0.0)
    # iterates through users with preferred categories first
    for user in users_with_preferences:
        total_left -= user.reinvest_pool
        reinvest_amount = user.reinvest_pool + min(0.0, total_left)
        pending_reinvestors.append((user, reinvest_amount))
        if total_left <= 0.0:
            break

    # if we still have money we want to reinvest, loop through users without preferences
    if total_left > 0.0:
        users_without_preferences = RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0)\
            .exclude(pk__in=users_with_preferences).order_by('user__last_name')
        for user in users_without_preferences:
            total_left -= user.reinvest_pool
            reinvest_amount = user.reinvest_pool + min(0.0, total_left)
            pending_reinvestors.append((user, reinvest_amount))
            if total_left <= 0.0:
                break
    for (user, amount) in pending_reinvestors:
        reinvestment = Payment(user=user,
                               project=instance.project,
                               entrant=instance.admin,
                               payment_type=PaymentType.objects.get_reinvestment_fragment(),
                               admin_reinvestment=instance,
                               amount=amount
                               )
        # user's reinvest_pool will be decremented on this Payment's save
        reinvestment.save()


@receiver(signals.post_save, sender=RepaymentFragment)
def post_save_repayment_fragment(**kwargs):
    """
    When a RepaymentFragment is saved, we increment the reinvest_pool in the
    related user.
    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    instance.user.reinvest_pool += float(instance.amount)
    instance.user.save()


@receiver(signals.pre_delete, sender=RepaymentFragment)
def pre_delete_repayment_fragment(**kwargs):
    """
    Before a RepaymentFragment is deleted, we decrement the reinvest_pool in the
    related user.
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool -= float(instance.amount)
    instance.user.save()


@receiver(signals.post_save, sender=Payment)
def post_save_payment(**kwargs):
    """
    If the payment is organic, we add this payment's user as a donor to the
    related project. If the payment is a reinvestment, we decrement the
    reinvest_pool in the related user.
    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    #if instance.is_organic:
    instance.project.donors.add(instance.user)
    if instance.payment_type == PaymentType.objects.get_reinvestment_fragment():
        instance.user.reinvest_pool -= float(instance.amount)
        instance.project.monthly_reinvestment_cap -= float(instance.amount)
        instance.user.save()


@receiver(signals.pre_delete, sender=Payment)
def pre_delete_payment(**kwargs):
    """
    Before a Payment is deleted, if it is a reinvestment, we increment the
    reinvest_pool in the related user.
    """
    instance = kwargs.get('instance')
    # if instance.is_organic:
    donation_count = instance.project.payment_set.filter(
                user=instance.user).count()
    if donation_count == 1:
        instance.project.donors.remove(instance.user)
    if instance.payment_type == PaymentType.objects.get_reinvestment_fragment():
        instance.user.reinvest_pool += float(instance.amount)
        instance.project.monthly_reinvestment_cap += float(instance.amount)
        instance.user.save()


@receiver(signals.post_delete, sender=Payment)
def post_delete_payment(**kwargs):
    """
    We need to cleanup here. If this related to UserReinvestment then just delete it.
    For AdminReinvestment we need some checking
    """
    instance = kwargs.get('instance')
    if instance.user_reinvestment:
        instance.user_reinvestment.delete()
    if instance.admin_reinvestment:
        admin_reinvestment = instance.admin_reinvestment
        admin_reinvestment.amount -= float(instance.amount)
        if admin_reinvestment.payment_set.all().count() == 0:
            admin_reinvestment.delete()


@receiver(signals.pre_init, sender=UserReinvestment)
def pre_init_user_reinvestment(**kwargs):
    """
    Raises a NotEnoughFundingException before __init__ if there are not enough
    funds for this UserReinvestment.
    """
    if not is_user_reinvestment_period():
        raise NotInUserReinvestmentPeriodException()

    init_kwargs = kwargs.get('kwargs')
    # can't initialize admin_repayment without required 'project' kwarg
    if not init_kwargs or not init_kwargs.get('user'):
        raise NotEnoughFundingException()
    user = init_kwargs['user']
    if user.reinvest_pool < 0.0:
        raise NotEnoughFundingException()


@receiver(signals.pre_save, sender=UserReinvestment)
def pre_save_user_reinvestment(**kwargs):
    """
    We cap the amount here by monthly allocation and funding goal itself
    We'll pick the minimum. Any balance we'll keep for the next cycle
    """
    instance = kwargs.get('instance')
    project = instance.project

    total_left = project.reinvest_amount_left
    if total_left <= 0.0:
        raise ProjectNotEligibleException()
    if total_left < float(instance.amount):
        instance.amount = total_left
    if instance.user.reinvest_pool < float(instance.amount):
        raise NotEnoughFundingException()


@receiver(signals.post_save, sender=UserReinvestment)
def post_save_user_reinvestment(**kwargs):
    """
    When an AdminReinvestment is saved, we pool as many donors as we need to
    fund the reinvestment, prioritizing users that have a preference for the
    Category of the project begin invested into. We only consider users that
    have a non-zero pool of investable money.

    """
    if not kwargs.get('created'):
        return
    instance = kwargs.get('instance')
    reinvestment = Payment(user=instance.user,
                           project=instance.project,
                           entrant=instance.user,
                           payment_type=PaymentType.objects.get_reinvestment_fragment(),
                           user_reinvestment=instance,
                           amount=instance.amount
                           )
        # user's reinvest_pool will be decremented on this Payment's save
    reinvestment.save()