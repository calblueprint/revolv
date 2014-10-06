from django.conf.urls import patterns, include, url
from django.contrib import admin

from revolv.base.views import HomePageView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'revolv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
)
