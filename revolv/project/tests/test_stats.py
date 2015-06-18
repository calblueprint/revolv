from django.test import SimpleTestCase
from revolv.project.stats import KilowattStatsAggregator


class StatsAggregatorTestCase(SimpleTestCase):
    def assert_stat_okay(self, stat):
        self.assertEqual(type(stat), float)
        self.assertNotEqual(stat, 0)

    def test_aggregator_works(self):
        """Test that none of the StatsAggregator functions error."""
        aggregator = KilowattStatsAggregator(12)
        self.assert_stat_okay(aggregator.pounds_carbon_saved_per_month)
        self.assert_stat_okay(aggregator.acres_of_trees_saved_per_year)
        self.assert_stat_okay(aggregator.dollars_saved_per_month)
        self.assert_stat_okay(aggregator.automobile_miles_per_month)
