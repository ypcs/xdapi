# -*- coding: utf-8 -*-
from django.contrib import admin
from shorturls.models import ShortURL

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('key', 'url', 'title', 'visit_count', 'status',)

admin.site.register(ShortURL, ShortURLAdmin)