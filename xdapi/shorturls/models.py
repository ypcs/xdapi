# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.conf import settings

_ = lambda x:x

SHORTURL_KEY_REGEX = r'^[\w\d:-]{3,255}'

class ShortURL(models.Model):
    SHORTURL_STATUS_CHOICES = (
        ('A', _('Active')),     # Created, in use
        ('R', _('Removed')),    # Removed, do not redirect
        ('S', _('Spam')),       # Marked as spam, do not redirect
        ('V', _('Verified')),   # Manually checked & verified, OK
        ('E', _('Expired')),    # Expired, do not redirect
        ('C', _('Confirm')),    # Confirm, that user really want's to continue
    )
    SHORTURL_DISABLED_STATUSES = ('R', 'S', 'E',)

    url = models.URLField(verbose_name='URL')
    key = models.CharField(max_length=255, unique=True, validators=[RegexValidator(regex=SHORTURL_KEY_REGEX)])

    title = models.CharField(max_length=255, blank=True, null=True)

    visit_count = models.PositiveIntegerField(editable=False, default=0)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    status = models.CharField(max_length=1, choices=SHORTURL_STATUS_CHOICES, default='A')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def is_redirectable(self):
        # TODO: Check this @ views.py
        if self.status in SHORTURL_DISABLED_STATUSES:
            return False
        return True

    def update_visits(self):
        self.visit_count += 1
        self.save()

    def __str__(self):
        return "%s => %s" % (self.key, self.url)

    class Meta:
        verbose_name = 'Short URL'
        verbose_name_plural = 'Short URLs'