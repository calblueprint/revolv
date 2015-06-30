"""
Module for encapsulating functions related to project statistics (aka
computing the effects of projects based on their stated kilowatt output).
"""
from django.db.models import Sum

class KilowattStatsAggregatorException(Exception):
    """Exception for something that went wrong with the KilowattStatsAggregator."""
    pass


class KilowattStatsAggregator(object):
    """
    A class to abstract the calculation of different energy statistics about a
    project, based on the kilowatt output of the project. The idea is that in order
    to engage donors, it makes sense for RE-volv to display the impact of a solar
    project in terms of not only power output but dollars saved per month, equivalent
    acres of trees that could be planted, etc.

    This is a utility class that takes in a kilowatt number (or, can accept instantiation
    from a Project or a Project queryset) and makes different statistics about the
    kilowatt power output available through calculations. Another advantage is that if
    we need to change the calculations, the price of electricity, or anything else
    related to the project stats, we can do so here and only here.

    Note: it's important to make the distinction between kilowatt output and kilowatt-hour
    output. Kilowatt (kW) is a measure of the power of the solar panel: i.e. its ability to
    produce energy. If you have a 25 kW solar panel array, then it will be able to produce
    a lot more electricity than a 1 kW solar panel array in the same amount of time (in fact,
    about 25x more). Apparently residential solar panels are usually between 5 and 25 kW,
    usually, at the time of writing.

    Kilowatt-hours (kWh), however, are a measure of energy (in this case, electric energy that comes
    through residential power outlets). A solar panel array rated at 1 kW power output will
    produce 1 kWh of electricty in one hour (this is why it's called a kilowatt-hour). If you're
    scientifically inclined, 1 kWh is equal to 3600 kilojoules, or the work done by a force
    of 3,600,000 newtons when the force is exerted over 1 meter, or the energy required to lift
    3,600,000 small apples into the air by one meter. See https://en.wikipedia.org/wiki/Kilowatt_hour and
    https://www.google.com/search?q=1+kwh+to+kj&ie=utf-8&oe=utf-8#safe=off&q=1+kilowatt+hour+to+kilojoules
    """
    # below are some constants which have been approximated based on various sources. it may
    # be necessary to update these periodically.

    # Price of electricity in CA is roughly 15.2 cents.
    # http://www.npr.org/sections/money/2011/10/27/141766341/the-price-of-electricity-in-your-state
    ELECTRICITY_PRICE_PER_KWH = 0.152  # dollars

    # Number of hours in a month, on average, is 730.484
    # https://www.google.com/search?q=hours+in+a+month&ie=utf-8&oe=utf-8
    NUM_HOURS_IN_MONTH = 730.484

    # Number of hours in a year, on average, is 8765.81
    # https://www.google.com/search?q=hours+in+a+uyear&ie=utf-8&oe=utf-8#safe=off&q=hours+in+a+year
    NUM_HOURS_IN_YEAR = 8765.81

    # One kWh is equal to 1.845 pounds of carbon emissions, roughly.
    # http://www.eia.gov/tools/faqs/faq.cfm?id=74&t=11
    POUNDS_CARBON_PER_KWH = 1.845

    # Planting one acre of trees reduces C02 in the air by an equivalent 5125 kWh
    # https://www.mtholyoke.edu/org/ccc/website/campaigns_energyconservation.html
    KWH_PER_ACRE_OF_TREES = 5125

    # 1 gallon of gas = 33.41 kWh with 2015 cars, on average
    # https://en.wikipedia.org/wiki/Gasoline_gallon_equivalent
    KWH_PER_GALLON_GAS = 33.41

    # http://www.huffingtonpost.com/2014/10/08/average-fuel-economy-record_n_5953968.html
    # the average mpg number may need to periodically be updated, as it is
    # prone to fast increase! Also note: this number accounts only for cars proudced in
    # 2015.
    AVERAGE_AMERICAN_MPG = 24.1

    # percentage of day the solar panels produce power is roughly 11.5 hours a day in CA:
    # http://aa.usno.navy.mil/cgi-bin/aa_durtablew.pl?form=1&year=2015&task=-1&state=CA&place=San+Francisco
    SOLAR_PANEL_USE_FACTOR_PER_DAY = 11.5 / 24

    @classmethod
    def from_project(cls, project):
        """Instantage an aggregator from a Project models."""
        return cls(project.impact_power)

    @classmethod
    def from_project_queryset(cls, queryset):
        """Instantiate an aggregator from a queryset of Projects."""
        total_kilowatts = queryset.aggregate(Sum("impact_power"))["impact_power__sum"]

        if total_kilowatts is None:
            raise KilowattStatsAggregatorException("Could not determine total kilowatt output of Project queryset.")

        return cls(queryset.aggregate(Sum("impact_power"))["impact_power__sum"])

    def __init__(self, kilowatts):
        """
        Instantiate the aggregator with a certain number of kilowatts.

        Note that here we use kilowatts instead of kilowatt-hours because if
        using kilowatt-hours, we'd have to pass in kilowatt-hours per month,
        or day, or year in order to do all the calculations, which might
        cause bugs due to increased abiguity of the units of the argument.
        Kilowatts, however, are not an abiguous unit and they're also in the
        name of this class, so we should be good on that front.
        """
        self.kilowatts = float(kilowatts)

    @property
    def kilowatt_hours_per_month(self):
        """Return the number of kilowatt hours outputted per month, given this aggregator's kilowatt value."""
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.SOLAR_PANEL_USE_FACTOR_PER_DAY
    
    @property
    def pounds_carbon_saved_per_month(self):
        """
        Return the pounds of carbon emissions per month equivalent to the aggregator's kilowatt value.

        According to http://www.eia.gov/tools/faqs/faq.cfm?id=74&t=11, the average pounds of carbon
        emitted via fossil fuels per kWh is 1.845: aka (2.07+2.15+2.17+1.21+1.67+1.80)/6. Thus the
        pounds of carbon saved per month is the number of kilowatt hours produced in a month times
        1.845.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.SOLAR_PANEL_USE_FACTOR_PER_DAY * self.POUNDS_CARBON_PER_KWH

    @property
    def dollars_saved_per_month(self):
        """
        Return the California dollars per month equivalent to the aggregator's kilowatt value.

        According to http://www.npr.org/sections/money/2011/10/27/141766341/the-price-of-electricity-in-your-state,
        the price of electricity per kilowatt hour is 0.152 dollars (15.2 cents) in California.
        According to https://www.google.com/search?q=hours+in+a+month&ie=utf-8&oe=utf-8, there are
        730.484 hours in a month. This means that the money that a n kilowatt solar panel will save
        is equal to n * 730.484 * 0.152.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.SOLAR_PANEL_USE_FACTOR_PER_DAY * self.ELECTRICITY_PRICE_PER_KWH

    @property
    def acres_of_trees_saved_per_year(self):
        """
        Return the acres of trees that take in the carbon equivalent to the aggregator's kilowatt
        value per year.

        According to https://www.mtholyoke.edu/org/ccc/website/campaigns_energyconservation.html,
        574000/112 = 5125 kWh are needed to equate to planting one acre of trees. According
        to https://www.google.com/search?q=hours+in+a+uyear&ie=utf-8&oe=utf-8#safe=off&q=hours+in+a+year
        there are 8765.81 hours in a year, so (acres of trees) = (kilowatts) * (hours in a year) / 5125
        """
        return self.kilowatts * self.NUM_HOURS_IN_YEAR * self.SOLAR_PANEL_USE_FACTOR_PER_DAY / self.KWH_PER_ACRE_OF_TREES

    @property
    def automobile_miles_per_month(self):
        """
        Return the automobile miles driven per month equivalent to the aggregator's kilowatt value
        based on the average MPG of cars produced in 2015.

        According to https://en.wikipedia.org/wiki/Gasoline_gallon_equivalent, a gallon of regular
        gasoline has equivalent energy to 33.41 kWh. Average fuel economy is roughly 24.1 mpg in America,
        according to http://www.huffingtonpost.com/2014/10/08/average-fuel-economy-record_n_5953968.html.
        So, (miles driven per month) = (kilowatts) * (num hours in month) / (num kWh per gal) * (average mpg).
        I knew taking ERG C100 would come in handy some day.

        TODO: could take into account old cars as well as 2015 cars when calculating the average MPG.
        """
        return self.kilowatts * self.NUM_HOURS_IN_MONTH * self.SOLAR_PANEL_USE_FACTOR_PER_DAY / self.KWH_PER_GALLON_GAS * self.AVERAGE_AMERICAN_MPG

    def as_dict(self):
        """Return all statistics as a dict."""
        return {
            "pounds_carbon_saved_per_month": self.pounds_carbon_saved_per_month,
            "dollars_saved_per_month": self.dollars_saved_per_month,
            "acres_of_trees_saved_per_year": self.acres_of_trees_saved_per_year,
            "automobile_miles_per_month": self.automobile_miles_per_month,
            "kilowatt_hours_per_month": self.kilowatt_hours_per_month,
            "kilowatts": self.kilowatts
        }
