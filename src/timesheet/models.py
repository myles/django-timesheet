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

PRINTABLE_CEO_CHOICES = (
	(10, "It's life-sustaining billable work!"),
	(10, "It's signing new business!"),
	(5, "It's publishable code! Ship it!"),
	(5, "It's sharp visual desgin! Show it!"),
	(5, "It's concrete planning or accounting!"),
	(2, "It's new self-promotion!"),
	(2, "It's a new article for the blog!"),
	(2, "It's a social or business development!"),
	(1, "It's maintaining an old relationship!"),
	(1, "It's making a new relationship!")
)

class Timesheet(models.Model):
	job = models.CharField(_('job'), max_length=200)
	date = models.DateField(_('date'))
	time = models.TimeField(_('time'))
	person = models.ForeignKey(User)
	hours = models.DecimalField(_('hours'), max_digits=4, decimal_places=2)
	
	pceo = models.IntegerField(_('Printable CEO'), blank=True, null=True,
		choices=PRINTABLE_CEO_CHOICES,
		help_text=_('When is something Worth Doing?'))
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
		return u"%s %s - %s" % (self.person.first_name, self.person.last_name, self.date)