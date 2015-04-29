from webtest import Upload


class ProjectFormFiller:
    """
    This is a webtest FormFiller that fills out a webtest form for an instance of
    revolv.project.models.Project. The point of this Filler is to fill out fields
    that django doesn't know what to do with in the regular ModelForm for Project:
    specifically, cover_photo, which is required by the project create page form
    but defaults to None in a ProjectFactory, and categories, which have a different
    name in the form than they do in the project model.

    This class accepts a partially filled webtest form and a project instance, and
    fills in the cover photo and categories fields and returns the filled form when
    fill() is called.

    This is a separate class rather than a part of WebTestMixin (from revolv.lib.testing.py)
    in order to facilitate more modularized filling of other ModelForms through webtest
    in the future.
    """

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
        form["cover_photo"] = Upload("revolv/lib/test_utils/test_cover_photo.jpg")
        form["categories_select"] = ["Health"]
        return form


FILLERS = {
    "Project": ProjectFormFiller
}
