from django.conf.urls import include, patterns, url
from django.contrib import admin
from revolv.base.views import (DashboardRedirect, HomePageView, LoginView,
                               LogoutView, SignInView, SignupView)

urlpatterns = patterns('',
                       url(r'^facebook/', include('django_facebook.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^project/', include('revolv.project.urls', namespace='project')),
                       url(r'^dashboard/$', DashboardRedirect.as_view(), name='dashboard'),
                       url(r'^dashboard/admin/', include('revolv.administrator.urls', namespace='administrator')),
                       url(r'^dashboard/ambassador/', include('revolv.ambassador.urls', namespace='ambassador')),
                       url(r'^dashboard/donor/', include('revolv.donor.urls', namespace='donor')),
                       url(r'^signin/$', SignInView.as_view(), name='signin'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^signup/$', SignupView.as_view(), name='signup'),
                       url(r'^logout/$', LogoutView.as_view(), name='logout'),
                       url(r'^', include('cms.urls')),
                       )
