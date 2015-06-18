from django.test import TestCase
from revolv.project.models import Project
from revolv.project.stats import KilowattStatsAggregator


class StatsAggregatorTestCase(TestCase):
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

    def test_auto_instantiations(self):
        """Test that we can create a StatsAggregator from projects or querysets."""
        aggregator = KilowattStatsAggregator.from_project(Project.factories.base.create(impact_power=12.0))
        self.assertEqual(aggregator.kilowatts, 12.0)

        project1, project2 = Project.factories.base.create_batch(2, impact_power=20.0)
        aggregator = KilowattStatsAggregator.from_project_queryset(Project.objects.filter(id__in=[project1.pk, project2.pk]))
        self.assertEqual(aggregator.kilowatts, 40.0)
