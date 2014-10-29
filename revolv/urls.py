import django.contrib.auth.views as auth_views
from django.conf.urls import include, patterns, url
from django.contrib import admin
from revolv.base.views import HomePageView, LoginView, SignInView, SignupView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'revolv.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       (r'^facebook/', include('django_facebook.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       url(r'^signin/$', SignInView.as_view(), name='signin'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^signup/$', SignupView.as_view(), name='login'),
                       url(
                           r'^logout/$',
                           auth_views.logout,
                           {"next_page": "/"},
                           name='logout'
                       ),
                       )
