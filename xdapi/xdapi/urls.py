from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from content.views import ContentView
from content.views import ContentView as UserContentView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xdapi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^~(?P<user>\w+)/(?P<key>' + settings.CONTENT_KEY_REGEX + ')$', UserContentView.as_view(), name='user-content'),
    url(r'^(?P<key>' + settings.CONTENT_KEY_REGEX + ')$', ContentView.as_view(), name='content'),
)
