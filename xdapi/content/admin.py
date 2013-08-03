# -*- coding: utf-8 -*-
from django.contrib import admin
from content.models import Content

# TODO: Allow searching by URL, for example "I wan't to see what keys link to this URL"

class ContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'content_type', 'title', 'url', 'owner', 'visit_count', 'status',)

admin.site.register(Content, ContentAdmin)