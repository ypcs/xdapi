# -*- coding: utf-8 -*-
from django.contrib import admin
from shorturls.models import ShortURL

# TODO: Allow searching by URL, for example "I wan't to see what keys link to this URL"

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('key', 'url', 'title', 'owner', 'visit_count', 'status',)

admin.site.register(ShortURL, ShortURLAdmin)