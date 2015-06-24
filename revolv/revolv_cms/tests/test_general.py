from django_webtest import WebTest


class GeneralTest(WebTest):
    def test_admin_pages_work(self):
        """
        Test that the app doesn't error when going to /cms/. Tests like
        this could have avoided https://github.com/calblueprint/revolv/issues/362
        """
        resp = self.app.get("/cms/").maybe_follow()
        self.assertEqual(resp.status_code, 200)
