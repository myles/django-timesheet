from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
import time

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation

class Timesheet(models.Model):
	subject = models.CharField(_('subject'), max_length=200)
	date = models.DateField(_('date'))
	person = models.ForeignKey(User)
	hours = models.DecimalField(_('hours'), max_digits=4, decimal_places=2)
	
	note = GenericRelation(Comment, object_id_field='object_pk')
	
	content_type = models.ForeignKey(ContentType, blank=True, null=True)
	object_id = models.PositiveIntegerField(blank=True, null=True)
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('timesheet')
		verbose_name_plural = _('timesheets')
		db_table = 'timesheets'
		ordering = ('-date', 'hours')
	
	def __unicode__(self):
		return u"%s %s - %s" % (self.user.first_name, self.user.last_name, self.date)