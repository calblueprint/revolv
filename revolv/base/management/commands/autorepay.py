from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from revolv.payments.models import AdminRepayment
from revolv.project.models import Project


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--override',
                    action='store_true',
                    dest='override',
                    default=False,
                    help='Forcibly run command on day other than 1st or 15th.'),
    )

    def handle(self, *args, **options):
        """
        Run this function from the command line with `python manage.py autorepay`.

        This command iterates through all completed projects and makes a
        repayments to each of them according to their respective
        MonthlyReinvestableAmount and MonthlyOrganizationalCost.

        A Repayment is only made towards a project if it hasn't already been
        fully repayed.

        This command is cron-ed to run on the 1st and 15th of every month. To
        run it on any other day, the `--override` flag must be supplied.
        """
        day = timezone.now().day
        if not any([day == 1, day == 15, options['override']]):
            raise CommandError("autorepay command can only be run on the 1st or 15th of every month unless the `--override` flag is supplied. use with caution")

        cur_year = timezone.now().year
        for proj in Project.objects.get_completed():
            if not proj.is_repaid:
                repayment = AdminRepayment(
                    reinvestable=(proj.monthlyreinvestableamount_set.get(year=cur_year).amount / 2),
                    organizational_cost=(proj.monthlyorganizationalcost_set.get(year=cur_year).amount / 2),
                    admin=None,
                    project=proj
                )
                repayment.save()
