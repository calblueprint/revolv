from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.base.users import is_ambassador
from revolv.project.views import (CreateProjectDonationView, CreateProjectView,
                                  PostFundingUpdateView, ProjectView,
                                  ReviewProjectView, UpdateProjectView)

urlpatterns = patterns(
    '',
    url(r'^create$', is_ambassador(CreateProjectView.as_view()), name='new'),
    url(r'^(?P<pk>\d+)/edit$', is_ambassador(UpdateProjectView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/review$', is_ambassador(ReviewProjectView.as_view()), name='review'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/donate$', login_required(CreateProjectDonationView.as_view()), name='donate'),
    url(r'^(?P<pk>\d+)/update$', is_ambassador(PostFundingUpdateView.as_view()), name='update'),
)
