from webtest import Upload


class ProjectFormFiller:
    """TODO: docs"""

    def __init__(self, form, project):
        self.partial_webtest_form = form
        self.project = project

    def fill_form(self):
        """
        Things we need to fill in that the automatic filler cannot:

        1. cover_photo
        2. categories_select
        """
        form = self.partial_webtest_form
        form["cover_photo"] = Upload("revolv/lib/test_utils/test_cover_photo.png")
        form["categories_select"] = ["Health"]
        return form


FILLERS = {
    "Project": ProjectFormFiller
}
