import django.contrib.auth.views as auth_views
from django.conf.urls import include, patterns, url
from django.contrib import admin

from revolv.base.views import (DashboardView, HomePageView, LoginView,
                               SignInView, SignupView)

urlpatterns = patterns('',
                       (r'^facebook/', include('django_facebook.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^project/', include('revolv.project.urls',
                                                 namespace='project')),
                       url(r'^users/', DashboardView.as_view(), 
                        name='dashboard'),
                       url(r'^signin/$', SignInView.as_view(), name='signin'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^signup/$', SignupView.as_view(), name='signup'),
                       url(r'^logout/$', auth_views.logout, {"next_page": "/"},
                           name='logout'),
                       )
