import datetime
from cStringIO import StringIO

import mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from revolv.project.models import (MonthlyOrganizationalCost,
                                   MonthlyReinvestableAmount, Project)


class AutoRepayTestCase(TestCase):
    def test_off_day(self):
        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(2016, 3, 4)):
            err_stream_fail = StringIO()
            try:
                call_command('autorepay', override=False, stderr=err_stream_fail)
                self.fail("shouldn't succeed")
            except SystemExit:
                pass

            call_command('autorepay', override=True)

    def test_amount(self):
        project = Project.factories.completed.create(funding_goal=1200)
        cur_year = timezone.now().year
        MonthlyReinvestableAmount(
            project=project,
            year=cur_year,
            amount=200
        ).save()
        MonthlyOrganizationalCost(
            project=project,
            year=cur_year,
            amount=100
        ).save()

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 100)  # half-monthly

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 200)

        a_long_time_ago_in_a_galaxy_far_far_away = 2100
        MonthlyReinvestableAmount(
            project=project,
            year=a_long_time_ago_in_a_galaxy_far_far_away,
            amount=1000
        ).save()
        MonthlyOrganizationalCost(
            project=project,
            year=a_long_time_ago_in_a_galaxy_far_far_away,
            amount=10000
        ).save()

        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(a_long_time_ago_in_a_galaxy_far_far_away, 3, 4)):
            call_command('autorepay', override=True)
            self.assertEquals(project.amount_repaid, 200 + 500)
            call_command('autorepay', override=True)
            self.assertEquals(project.amount_repaid, 200 + 1000)

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 200 + 1000)
        self.assertTrue(project.is_repaid)
