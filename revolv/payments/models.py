from django.contrib.auth.models import User
from django.db import models
from revolv.project.models import Project

INSTRUMENT_PAYPAL = 'paypal'
INSTRUMENT_CHECK = 'check'


class PaymentInstrumentType(models.Model):
    """
        Abstraction for a payment instrument. (e.g. Paypal)
    """
    name = models.CharField(max_length=80, unique=True)


class PaymentTransaction(models.Model):
    """
        Abstraction indicating one particular payment.
    """
    payment_instrument_type = models.ForeignKey(PaymentInstrumentType)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    amount = models.FloatField()


class Donation(models.Model):
    """
        Abstraction of a donation from a user.
    """
    payment_transaction = models.ForeignKey(PaymentTransaction)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)
