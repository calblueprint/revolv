from django.conf.urls import patterns, url
from revolv.base.users import is_ambassador
from revolv.project.views import (CreateProjectView, PostFundingUpdateView,
                                  ProjectView, ReviewProjectView,
                                  SubmitDonationView, UpdateProjectView, PostProjectUpdateView)

urlpatterns = patterns(
    '',
    url(r'^create$', is_ambassador(CreateProjectView.as_view()), name='new'),
    url(r'^(?P<pk>\d+)/edit$', is_ambassador(UpdateProjectView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/review$', is_ambassador(ReviewProjectView.as_view()), name='review'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/donation/submit$', SubmitDonationView.as_view(), name="donation_submit"),
    url(r'^(?P<pk>\d+)/update$', is_ambassador(PostProjectUpdateView.as_view()), name='update'),
)
