from django.conf.urls import patterns, url
from revolv.administrator.views import AdministratorDashboardView
from revolv.base.users import is_administrator

urlpatterns = patterns(
    '',
    url(r'^$', is_administrator(AdministratorDashboardView.as_view()), name='dashboard'),
)
