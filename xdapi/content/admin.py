# -*- coding: utf-8 -*-
from django.contrib import admin
from content.models import URLContent

# TODO: Allow searching by URL, for example "I wan't to see what keys link to this URL"

class URLAdmin(admin.ModelAdmin):
    list_display = ('key', 'url', 'title', 'owner', 'visit_count', 'status',)

admin.site.register(URLContent, URLAdmin)