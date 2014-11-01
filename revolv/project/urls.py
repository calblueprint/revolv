from django.conf.urls import include, patterns, url

from revolv.project.views import (CreateProjectView, ProjectView,
                                  UpdateProjectView)

urlpatterns = patterns('',
    url(r'^create$', CreateProjectView.as_view(), name='new'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateProjectView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view')
)
