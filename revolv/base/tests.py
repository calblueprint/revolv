from django.test import TestCase


class SmokeTestCase(TestCase):
    def test_works(self):
        """Test that the test framework works."""
        self.assertEqual(1, 1)
