from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.base.users import is_ambassador
from revolv.project.views import (CreateProjectView, PostFundingUpdateView,
                                  ProjectView, ReviewProjectView,
                                  UpdateProjectView, submit_payment,
                                  validate_payment)

urlpatterns = patterns(
    '',
    url(r'^create$', is_ambassador(CreateProjectView.as_view()), name='new'),
    url(r'^(?P<pk>\d+)/edit$', is_ambassador(UpdateProjectView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+)/review$', is_ambassador(ReviewProjectView.as_view()), name='review'),
    url(r'^(?P<pk>\d+)/$', ProjectView.as_view(), name='view'),
    url(r'^(?P<pk>\d+)/payment/validate$', validate_payment),
    url(r'^(?P<pk>\d+)/payment/submit$', submit_payment),
    url(r'^(?P<pk>\d+)/update$', is_ambassador(PostFundingUpdateView.as_view()), name='update'),
)
