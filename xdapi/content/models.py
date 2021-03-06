# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError

from bs4 import BeautifulSoup
import requests
import reversion

from taggit.managers import TaggableManager

_ = lambda x:x

# TODO: Add support for OpenGraph

CONTENT_TYPE_URL = 'U'
CONTENT_TYPE_PASTE = 'P'
CONTENT_TYPE_FILE = 'F'
CONTENT_TYPES = (
    (CONTENT_TYPE_PASTE, _('Pastebin')),
    (CONTENT_TYPE_URL, _('URL Redirect')),
    ('W', _('Webshots')),
    (CONTENT_TYPE_FILE, _('File Upload')),
)

CONTENT_KEY_REGEX = r'^[\w\d:-]{3,255}'
CONTENT_KEY_RANDOM_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz01234567890'

CONTENT_STATUS_FAILURE = 'f'
CONTENT_STATUS_ACTIVE = 'A'
CONTENT_STATUS_EXPIRED = 'E'
CONTENT_STATUS_SPAM = 'S'
CONTENT_STATUS_REMOVED = 'R'
CONTENT_STATUS_VERIFIED = 'V'
CONTENT_STATUS_PRIVATE = 'P'

# Allowed statuses
CONTENT_STATUS_CHOICES = (
    (CONTENT_STATUS_ACTIVE, _('Active')), # Created, in use
    (CONTENT_STATUS_REMOVED, _('Removed')), # Removed, do not redirect
    (CONTENT_STATUS_SPAM, _('Spam')), # Marked as spam, do not redirect
    (CONTENT_STATUS_VERIFIED, _('Verified')), # Manually checked & verified, OK
    (CONTENT_STATUS_EXPIRED, _('Expired')), # Expired, do not redirect
    (CONTENT_STATUS_FAILURE, _('Failure')), # Has raised automatically detected failure
    (CONTENT_STATUS_PRIVATE, _('Private')), # Private content, owner must be logged in to access
)

# Which content should raise error?
CONTENT_DISABLED_STATUSES = (
    CONTENT_STATUS_REMOVED,
    CONTENT_STATUS_SPAM,
    CONTENT_STATUS_EXPIRED,
)

# What statuses are we allowed automatically redirect user to
CONTENT_ALLOW_REDIRECT_STATUSES = (
    CONTENT_STATUS_VERIFIED,
)

MIME_TYPE_DEFAULT = 'text/plain'

class Content(models.Model):

    
    content_type = models.CharField(max_length=1, choices=CONTENT_TYPES)
    key = models.CharField(max_length=255, unique=True, validators=[RegexValidator(regex=settings.CONTENT_KEY_REGEX)])
    #key = AutoSlugField(editable=True, blank=True, unique=True, populate_from=['title', 'content'], validators=[RegexValidator(regex=settings.CONTENT_KEY_REGEX)])

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.URLField(verbose_name='URL', blank=True, null=True)
    uploaded_file = models.FileField(upload_to='content/uploads', blank=True, null=True)

    password = models.CharField(max_length=255, blank=True, null=True)
    mime_type = models.CharField(max_length=255, default=MIME_TYPE_DEFAULT, verbose_name=_('MIME type'))

    #visit_count = models.PositiveIntegerField(editable=False, default=0)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    status = models.CharField(max_length=1, choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_ACTIVE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    tags = TaggableManager()

    def get_tags(self):
        return self.tags.get_query_set()
    get_tags.short_description = _('Tags')

    def get_tags_names(self):
        return [str(x) for x in self.get_tags()]
    get_tags_names.short_description = _('Tags')

    def get_tags_labels(self):
        return " ".join(['<span class="label">' + x + '</span>' for x in self.get_tags_names()])
    get_tags_labels.short_description = _('Tags')
    get_tags_labels.allow_tags = True

    def get_page_title(self):
        # TODO: Fetch page meta: og:title, og:sitename, og:description
        try:
            req = requests.get(self.url)
            if req.status_code == requests.codes.ok:
                soup = BeautifulSoup(req.text)
                return soup.title.string
            else:
                return ""
        except requests.exceptions.ConnectionError:
            self.status = CONTENT_STATUS_FAILURE
            return ""

    def clean(self):
        if self.content_type == CONTENT_TYPE_URL:
            if self.url is None or self.url == '':
                raise ValidationError(_("You must specify URL when creating URL redirections!"))
        elif self.content_type == CONTENT_TYPE_FILE:
            if self.uploaded_file is None or self.uploaded_file == '':
                raise ValidationError(_("You must upload file when creating file uploads!"))
        elif self.content_type == CONTENT_TYPE_PASTE:
            if self.content is None or self.content == '':
                # TODO: Allow fetching content from URL
                raise ValidationError(_("You must specify content when creating paste!"))

    def save(self, *args, **kwargs):
        # TODO: If pastebin, if URL has been set and no content, fetch content from url
        # TODO: If no title and has url, fetch title from it (or at least, try!)
        if self.content_type == CONTENT_TYPE_URL and self.title == "" and self.url != "":
            self.title = self.get_page_title()
        super(Content, self).save(*args, **kwargs)

    def __str__(self):
        return "%s: %s" % (self.key, self.title)

    def __unicode__(self):
        return self.__str__()

    class Meta:
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")
reversion.register(Content)