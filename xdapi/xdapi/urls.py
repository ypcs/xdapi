from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from shorturls.views import ShortURLRedirectView
from shorturls.models import SHORTURL_KEY_REGEX

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xdapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<key>' + SHORTURL_KEY_REGEX + ')$', ShortURLRedirectView.as_view(), name='shorturl'),

    url(r'^admin/', include(admin.site.urls)),
)
