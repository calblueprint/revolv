import mock
import json
from django.test import TestCase
from django_webtest import WebTest
from revolv.lib.testing import TestUserMixin, UserTestingMixin
from revolv.project.models import Project, ProjectUpdate


class PostProjectUpdatesTest(TestUserMixin, UserTestingMixin, TestCase):

    def helper_test_create_update_ambassador_administrator(self):
        """
        Tests that administrators and ambassadors can create project updates.
        """
        response = self.send_test_user_login_request()
        self.assertUserAuthed(response)
        project = Project.factories.base.create()
        response = self.client.post('/project/%d/update' % project.pk, {'update_text': 'This is an update'})
        new_updates = ProjectUpdate.objects.filter(update_text = 'This is an update')
        self.assertEqual(len(new_updates),1)
        self.assertEqual(new_updates[0].project, project)

    def test_admin_form_submission(self):
        """
        Tests that administrators can create project updates.
        """
        self.test_profile.make_administrator()
        self.helper_test_create_update_ambassador_administrator()

    def test_ambassador_form_submission(self):
        """
        Tests that ambassadors can create project updates.
        """
        self.test_profile.make_ambassador()
        self.helper_test_create_update_ambassador_administrator()

    def test_donor_form_submission(self):
        """
        Tests that donors can't create project updates.
        """
        self.test_profile.make_donor()
        response = self.send_test_user_login_request()
        self.assertUserAuthed(response)
        project = Project.factories.base.create()
        response = self.client.post('/project/%d/update' % project.pk, {'update_text': 'This is an update'})
        
        #the deny_access method is called in the view from the userdatamixin, which returns a redirect to the homepage
        self.assertEqual(response.status_code, 302)
        
class EditProjectUpdatesTest(TestUserMixin, UserTestingMixin, TestCase):

    def _make_update(self, project, text):
        """
        Makes an update to of given text to the given project.
        """
        response = self.send_test_user_login_request()
        self.assertUserAuthed(response)
        #response = self.client.post('/project/%d/update' % project.pk, {'update_text': text})
        ProjectUpdate(project = project, update_text = text).save()
        new_updates = ProjectUpdate.objects.filter(update_text = text)
        return new_updates[0]

    def _helper_test_edit_update(self, donor = False):
        """
        Tests that the administrator and ambassador can make updates. 
        """
        project = Project.factories.base.create()
        update = self._make_update(project, "This update has not been changed.")

        response = self.client.post('/project/editupdate/%d' % update.pk,
                        {'update_text': 'This update has been changed.'})

        old_update_text_updates = ProjectUpdate.objects.filter(update_text="This update has not been changed.")
        new_updates = ProjectUpdate.objects.filter(update_text="This update has been changed.")

        if not donor:
            self.assertEqual(len(old_update_text_updates), 0)
            self.assertEqual(update.project, new_updates[0].project)
            self.assertEqual(new_updates[0].update_text, "This update has been changed.")
        else:
            #the donor should be denied access and redirected
            self.assertEqual(response.status_code, 302)

    def test_edit_update_administrator(self):
        """
        Tests that a change is made to an update for an administrator.
        """
        self.test_profile.make_administrator()
        self._helper_test_edit_update()

    def test_edit_update_ambassador(self):
        """
        Tests that a change is made to an update for an ambassador.
        """
        self.test_profile.make_ambassador()
        self._helper_test_edit_update()

    def test_edit_update_donor(self):
        """
        Tests that a donor can't change an update.
        """
        self.test_profile.make_donor()
        self._helper_test_edit_update(True)

class DonationAjaxTestCase(TestUserMixin, TestCase):
    """
    Test suite for AJAX payment donations for projects.
    """
    DONATION = 'donation/submit'

    def setUp(self):
        super(DonationAjaxTestCase, self).setUp()
        self.send_test_user_login_request()
        self.project = Project.factories.base.create(project_status=Project.ACTIVE)

    def perform_valid_donation(self):
        """
        Utility method for performing a valid donation. Returns the response.
        """
        valid_donation = {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
            'type': 'visa',
            'first_name': 'William',
            'last_name': 'Taft',
            'expire_month': 6,
            'expire_year': 2020,
            'cvv2': '00',
            'number': '1234123412341234',
            'amount': '10.00',
        }
        return self.client.post(
            self.project.get_absolute_url() + self.DONATION,
            data=valid_donation,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_valid_donation(self):
        """
        Test valid donation via AJAX to /project/<pk>/donation/submit.
        """
        resp = self.perform_valid_donation()
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIsNone(content.get('error'))
        self.assertIsNotNone(self.project.donors.get(pk=self.test_user.pk))

    @mock.patch('revolv.lib.mailer.EmailMultiAlternatives')
    def test_post_donation_email(self, mock_mailer):
        """
        Tests whether a valid donation will send a revolv email
        """
        resp = self.perform_valid_donation()
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIsNone(content.get('error'))
        self.assertIsNotNone(self.project.donors.get(pk=self.test_user.pk))
        self.assertTrue(mock_mailer.called)
        # checks that the email address sent using mock mailer matches the user who donatred
        args, kwargs = mock_mailer.call_args
        self.assertEqual(kwargs['to'], ["john@example.com"])

    def test_invalid_donation_ajax(self):
        """
        Tests that invalid donation appropriately errors with on
        /donation/submit endpoint.
        """
        invalid_donation = {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
            'type': 'visa',
            # 'first_name': '',
            'last_name': 'Taft',
            'expire_month': 6,
            'expire_year': 2020,
            'cvv2': '00',
            'number': 'not a number',
            'amount': '10.00',
        }
        resp = self.client.post(
            self.project.get_absolute_url() + self.DONATION,
            data=invalid_donation,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertIsNotNone(content['error'])
