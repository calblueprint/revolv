from django.test.utils import override_settings
from django_webtest import WebTest


class GeneralTest(WebTest):

    def test_admin_pages_work(self):
        """
        Test that the app doesn't error when going to /cms/. Tests like
        this could have avoided https://github.com/calblueprint/revolv/issues/362
        """
        resp = self.app.get("/cms/").maybe_follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(DEBUG=False, COMPRESS_ENABLED=True)
    def test_admin_pages_work_with_django_compressor(self):
        """
        Test that the cms admin page doesn't error when django-compressor
        is enabled. Django-compressor is a dependency for wagtail, but
        it behaves differently with regards to staticfiles on local
        and staging/prod, resulting in https://github.com/calblueprint/revolv/issues/362
        This test exposes that error.
        """
        resp = self.app.get("/cms/").maybe_follow()
        self.assertEqual(resp.status_code, 200)
