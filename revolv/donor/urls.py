from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.donor.views import DonorDashboardView
from revolv.administrator.views import AdministratorAccountingView

urlpatterns = patterns(
    '',
    url(r'^$', login_required(DonorDashboardView.as_view()), name='dashboard'),
    url(r'^accounting$', AdministratorAccountingView.as_view(), name='accounting'),
)
