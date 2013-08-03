# -*- coding: utf-8 -*-
from django.contrib import admin
from content.models import Content
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import reversion
# TODO: Allow searching by URL, for example "I wan't to see what keys link to this URL"
# TODO: If superuser, allow editing status
# TODO: If superuser, allow editing owner
# TODO: Add "view" (ie. visit content page) link to list view

_ = lambda x:x

class ContentAdmin(reversion.VersionAdmin):
    list_display = ('key', 'content_type', 'title', 'url', 'owner', 'status', 'tags', 'mime_type',)
    fieldsets = [
        (None, {'fields': ['content_type', 'key', 'title', 'description', 'content', 'url', 'uploaded_file',],}),
        (_('Additional Details'), {'fields': ['tags', 'status', 'owner', 'password', 'mime_type',], 'classes': ['collapse',],})
    ]

    def save_model(self, request, obj, form, change):
        """Save user information"""
        obj.owner = request.user
        super(ContentAdmin, self).save_model(request=request, obj=obj, form=form, change=change)

    def queryset(self, request):
        """Show only users own content, unless superuser"""
        qs = super(ContentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:content_content_changelist'))
        return super(ContentAdmin, self).change_view(request, object_id, form_url, extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:content_content_changelist'))
        return super(ContentAdmin, self).delete_view(request, object_id, extra_context)

    def history_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:content_content_changelist'))
        return super(ContentAdmin, self).history_view(request, object_id, extra_context)

admin.site.register(Content, ContentAdmin)