from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.donor.views import DonorDashboardView, AccountingView, AccountingPartialView

urlpatterns = patterns(
    '',
    url(r'^$', login_required(DonorDashboardView.as_view()), name='dashboard'),
    url(r'^accounting$', AccountingView.as_view(), name='accounting'),
    url(r'^accounting/partial$', AccountingPartialView.as_view(), name='accountingPartial')
)
