# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView, RedirectView

#from shorturls.models import ShortURL

class ContentView(TemplateView):
    pass

#class ShortURLRedirectView(RedirectView):
#    def get_redirect_url(self, key):
#        shorturl = get_object_or_404(ShortURL, key=key)
#        shorturl.update_visits()
#        return shorturl.url
