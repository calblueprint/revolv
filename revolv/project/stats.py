"""
Module for encapsulating functions related to project statistics (aka
computing the effects of projects based on their stated kilowatt output).
"""
from django.db.models import Sum


class KilowattStatsAggregatorException(Exception):
    pass


class KilowattStatsAggregator(object):
    ELECTRICITY_PRICE_PER_KWH = 0.152  # dollars
    NUM_HOURS_IN_MONTH = 730.484
    NUM_HOURS_IN_YEAR = 8765.81
    POUNDS_CARBON_PER_KWH = 1.845
    KWH_PER_ACRE_OF_TREES = 5125
    KWH_PER_GALLON_GAS = 33.41
    # the average mpg number may need to periodically be updated, as it is
    # prone to fast increase!
    AVERAGE_AMERICAN_MPG = 24.1

    @classmethod
    def from_project(cls, project):
        return cls(project.impact_power)

    @classmethod
    def from_project_queryset(cls, queryset):
        total_kilowatts = queryset.aggregate(Sum("impact_power"))["impact_power__sum"]

        if total_kilowatts is None:
            raise KilowattStatsAggregatorException("Could not determine total kilowatt output of Project queryset.")

        return cls(queryset.aggregate(Sum("impact_power"))["impact_power__sum"])

    def __init__(self, kilowatts):
        self.kilowatts = float(kilowatts)

    @property
    def pounds_carbon_saved_per_month(self):
        """
        According to http://www.eia.gov/tools/faqs/faq.cfm?id=74&t=11, the average pounds of carbon
        emitted via fossil fuels per kWh is 1.845: aka (2.07+2.15+2.17+1.21+1.67+1.80)/6. Thus the
        pounds of carbon saved per month is the number of kilowatt hours produced in a month times
        1.845.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.POUNDS_CARBON_PER_KWH

    @property
    def dollars_saved_per_month(self):
        """
        According to http://www.npr.org/sections/money/2011/10/27/141766341/the-price-of-electricity-in-your-state,
        the price of electricity per kilowatt hour is 0.152 dollars (15.2 cents) in California.
        According to https://www.google.com/search?q=hours+in+a+month&ie=utf-8&oe=utf-8, there are
        730.484 hours in a month. This means that the money that a n kilowatt solar panel will save
        is equal to n * 730.484 * 0.152.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.ELECTRICITY_PRICE_PER_KWH

    @property
    def acres_of_trees_saved_per_year(self):
        """
        According to https://www.mtholyoke.edu/org/ccc/website/campaigns_energyconservation.html,
        574000/112 = 5125 kWh are needed to equate to planting one acre of trees. According
        to https://www.google.com/search?q=hours+in+a+uyear&ie=utf-8&oe=utf-8#safe=off&q=hours+in+a+year
        there are 8765.81 hours in a year, so (acres of trees) = (kilowatts) * (hours in a year) / 5125
        """
        return self.kilowatts * self.NUM_HOURS_IN_YEAR / self.KWH_PER_ACRE_OF_TREES

    @property
    def automobile_miles_per_month(self):
        """
        According to https://en.wikipedia.org/wiki/Gasoline_gallon_equivalent, a gallon of regular
        gasoline has equivalent energy to 33.41 kWh. Average fuel economy is roughly 24.1 mpg in America,
        according to http://www.huffingtonpost.com/2014/10/08/average-fuel-economy-record_n_5953968.html.
        So, (miles driven per month) = (kilowatts) * (num hours in month) / (num kWh per gal) * (average mpg).
        I knew taking ERG C100 would come in handy some day.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH / self.KWH_PER_GALLON_GAS * self.AVERAGE_AMERICAN_MPG
