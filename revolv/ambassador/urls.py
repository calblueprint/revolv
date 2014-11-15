from django.conf.urls import patterns, url
from revolv.ambassador.views import AmbassadorDashboardView
from revolv.base.users import is_ambassador

urlpatterns = patterns(
    '',
    url(r'^$', is_ambassador(AmbassadorDashboardView.as_view()), name='dashboard'),
)
