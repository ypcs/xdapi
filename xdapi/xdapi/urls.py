from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shorturls.views import ShortURLRedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xdapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<key>\w+)$', ShortURLRedirectView.as_view(), name='shorturl'),

    url(r'^admin/', include(admin.site.urls)),
)
