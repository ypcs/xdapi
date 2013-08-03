from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from content.views import ContentView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xdapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<key>' + settings.CONTENT_KEY_REGEX + ')$', ContentView.as_view(), name='content'),
)
