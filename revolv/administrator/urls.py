from django.conf.urls import patterns, url

from revolv.administrator.views import (admin_email_csv_download,
                                        AdministratorDashboardView,
                                        AdministratorEmailView,
                                        AdministratorAccountingView,
                                        AdministratorAddAdjustmentView,
                                        AccountingJSONView)
from revolv.base.users import is_administrator

urlpatterns = patterns(
    '',
    url(r'^$', is_administrator(AdministratorDashboardView.as_view()), name='dashboard'),
    url(r'^email$', is_administrator(AdministratorEmailView.as_view()), name='email'),
    url(r'^email/csv$', admin_email_csv_download, name='emailcsv'),
    url(r'^accounting$', is_administrator(AdministratorAccountingView.as_view()), name='accounting'),
    url(r'^accounting/adjustment$', is_administrator(AdministratorAddAdjustmentView.as_view()), name='adjustment'),
    url(r'^accounting/json$', AccountingJSONView.as_view(), name='accountingJSON')
)
