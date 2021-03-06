# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, RedirectView

#from shorturls.models import ShortURL
from content.models import Content

# TODO: If shorturl, and autoredirect & redirect allowed => return redirect url
# TODO: If other content, or autoredirect disabled, or redirect not allowed => display preview
# TODO: Fileuploads: create CF urls w/ access token, locked to specific IP, and set access time to 10min etc., ie. force using our site to access

class ContentView(TemplateView):
    template_name = 'content/view_content.html'

    def get_context_data(self, **kwargs):
        context = super(ContentView, self).get_context_data(**kwargs)
        context['obj'] = get_object_or_404(Content, **kwargs)
        return context

#class ShortURLRedirectView(RedirectView):
#    def get_redirect_url(self, key):
#        shorturl = get_object_or_404(ShortURL, key=key)
#        shorturl.update_visits()
#        return shorturl.url
