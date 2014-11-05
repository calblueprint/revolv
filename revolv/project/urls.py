from django.conf.urls import patterns, url
from revolv.project.views import (CreateProjectDonationView, CreateProjectView,
                                  ProjectView, ReviewProjectView,
                                  UpdateProjectView)

urlpatterns = patterns(
    '',
    url(r'^create$', CreateProjectView.as_view(), name='new'),
    url(r'^edit/(?P<pk>\d+)/$', UpdateProjectView.as_view(), name='edit'),
    url(r'^review/(?P<pk>\d+)/$', ReviewProjectView.as_view(), name='review'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/donate$', CreateProjectDonationView.as_view(), name='donate'),
)
