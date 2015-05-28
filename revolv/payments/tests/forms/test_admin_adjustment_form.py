import mock
from django.test import TestCase
from revolv.administrator.forms import AdjustmentForm
from revolv.payments.models import AdminAdjustment

class AdminAdjustmentFormTestCase(TestCase):

    def test_valid_form(self):
        """Verify that a valid form is valid."""
        adjustment_form = AdjustmentForm({
        		'name': 'Salaries',
        		'amount': '4000',
        		'created_at': '2015-02-02',
        		'cash_type': 'cash_in'
        	})
        self.assertTrue(adjustment_form.is_valid())