from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from revolv.base import views as base_views

urlpatterns = patterns(
    '',
    (r'^ckeditor/', include('ckeditor.urls')),  # for assets for the ckedit widget, etc
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', base_views.HomePageView.as_view(), name='home'),
    url(r'^project/', include('revolv.project.urls', namespace='project')),
    url(r'^dashboard/$', base_views.DashboardRedirect.as_view(), name='dashboard'),
    url(r'^dashboard/categories/$', base_views.CategoryPreferenceSetterView.as_view(), name='dashboard_category_setter'),
    url(r'^dashboard/admin/', include('revolv.administrator.urls', namespace='administrator')),
    url(r'^dashboard/ambassador/', include('revolv.ambassador.urls', namespace='ambassador')),
    url(r'^dashboard/donor/', include('revolv.donor.urls', namespace='donor')),

    url(r'^what-we-do/projects/', base_views.ProjectListView.as_view(), name='projects_list'),
    url(r'^signin/$', base_views.SignInView.as_view(), name='signin'),
    url(r'^login/$', base_views.LoginView.as_view(), name='login'),
    url(r'^signup/$', base_views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', base_views.LogoutView.as_view(), name='logout'),
    url(r'^unsubscribe/(?P<action>\w+)/$', 'revolv.base.views.unsubscribe', name='unsubscribe'),
    url(r'^my_social_account/$', 'revolv.base.views.social_connection', name='social-connection'),
    url(r'^social_connect_failed/$', 'revolv.base.views.social_exception', name='social-exception'),

    url(r'^password_reset/$', base_views.password_reset_initial, name="password_reset"),
    url(r'^password_reset/done/$', base_views.password_reset_done, name="password_reset_done"),
    url(r'^password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$$', base_views.password_reset_confirm, name="password_reset_confirm"),
    url(r'^password_reset/complete/$', base_views.password_reset_complete, name="password_reset_complete"),
    url(r'^password_change/$', base_views.password_change, name="password_change"),

    # wagtail urls, see http://wagtail.readthedocs.org/en/v1.0b2/howto/settings.html
    # note: we're not including the search module for public users, so we don't define it here
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'social/', include('social.apps.django_app.urls', namespace='social')),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism

    url(r'', include(wagtail_urls)),

)

if settings.MEDIA_SERVE_LOCALLY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)