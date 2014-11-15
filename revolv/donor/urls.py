from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from revolv.donor.views import DonorDashboardView

urlpatterns = patterns(
    '',
    url(r'^$', login_required(DonorDashboardView.as_view()), name='dashboard'),
)
