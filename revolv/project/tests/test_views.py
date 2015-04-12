from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.project.models import Project
from revolv.lib.testing import TestUserMixin, UserTestingMixin

class RequestTest(TestCase):
    """Test that all is well with the project pages."""

    def _assert_project_page_works(self, project):
        resp = self.client.get(project.get_absolute_url())
        self.assertNotEqual(resp.status_code, 500)

    def test_project_page(self):
        project = Project.factories.base.create()

        for status_choice in Project.PROJECT_STATUS_CHOICES:
            status = status_choice[0]
            project.project_status = status
            project.save()
            self._assert_project_page_works(project)

    def test_drafted_projects_404(self):
        """Test that the response is 404 when trying to request the page of a drafted project."""
        project = Project.factories.base.create(project_status=Project.DRAFTED)
        resp = self.client.get(project.get_absolute_url())
        self.assertEqual(resp.status_code, 404)