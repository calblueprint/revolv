import datetime
import os

import mock
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone
from revolv.project.models import (MonthlyOrganizationalCost,
                                   MonthlyReinvestableAmount, Project)


class AutoRepayTestCase(TestCase):
    def test_off_day(self):
        """
        Tests that the `autorepay` command only runs successfully on the 1st and
        15th of every month. The command must fail on any other day *unless* the
        `--override` flag is given from the command line.
        """
        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(2016, 3, 4)):
            try:
                with open(os.devnull, 'w') as f:
                    call_command('autorepay', stderr=f, override=False)
                self.fail("autorepay command shouldn't succeed on an off day if the `override` flag is not set")
            except CommandError:
                pass

            call_command('autorepay', override=True)

    def test_amount(self):
        """
        Tests that the `autorepay` command repays the correct amount. Since the
        command runs twice per month, on any given run of the command, it should
        repay all qualified projects by (MonthlyReinvestableAmount / 2).
        """
        project = Project.factories.completed.create(funding_goal=1200)
        MonthlyReinvestableAmount.factories.base.create(
            project=project,
            amount=200
        )
        MonthlyOrganizationalCost.factories.base.create(
            project=project,
            amount=100
        ).save()

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 100)  # half-monthly

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 200)

        a_long_time_ago_in_a_galaxy_far_far_away = 2100
        MonthlyReinvestableAmount.factories.base.create(
            project=project,
            year=a_long_time_ago_in_a_galaxy_far_far_away,
            amount=1000
        )
        MonthlyOrganizationalCost.factories.base.create(
            project=project,
            year=a_long_time_ago_in_a_galaxy_far_far_away,
            amount=10000
        )

        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(a_long_time_ago_in_a_galaxy_far_far_away, 3, 4)):
            call_command('autorepay', override=True)
            self.assertEquals(project.amount_repaid, 200 + 500)
            call_command('autorepay', override=True)
            self.assertEquals(project.amount_repaid, 200 + 1000)

        call_command('autorepay', override=True)
        self.assertEquals(project.amount_repaid, 200 + 1000)
        self.assertTrue(project.is_repaid)
