from django.conf.urls import include, patterns, url
from django.contrib import admin
from revolv.base.views import HomePageView, SignInView
from revolv.project.views import (CreateProjectView, ProjectView,
                                  UpdateProjectView)

urlpatterns = patterns('',
                       (r'^facebook/', include('django_facebook.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^project/create$', CreateProjectView.as_view(),
                           name='project-new'),
                       url(r'^project/edit/(?P<pk>\d+)/$',
                           UpdateProjectView.as_view(),
                           name='project-edit'),
                       url(r'^project/(?P<pk>\d+)/$', ProjectView.as_view(),
                           name='project-view'),
                       url(r'^signin/$', SignInView.as_view(), name='signin'),
                       )


# Examples:
# url(r'^$', 'revolv.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
