from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.project.views import (CreateProjectDonationView, CreateProjectView,
                                  ProjectView, ReviewProjectView,
                                  UpdateProjectView)

urlpatterns = patterns(
    '',
    url(r'^create$', login_required(CreateProjectView.as_view()), name='new'),
    url(r'^(?P<pk>\d+)/edit$', login_required(UpdateProjectView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/review$', login_required(ReviewProjectView.as_view()), name='review'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/donate$', CreateProjectDonationView.as_view(), name='donate'),
)
