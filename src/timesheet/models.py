from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
import time

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericRelation

class Manager(models.Model):
	manager = models.ForeignKey(User, related_name='manager',
		unique=True)
	employee = models.ManyToManyField(User, related_name='employees')
	
	class Meta:
		verbose_name = _('manager')
		verbose_name_plural = _('managers')
		db_table = 'timesheet_managers'
	
	@permalink
	def get_absolute_url(self):
		return ('timesheet_manager_detail', None, {
			'username': self.manager.username,
		})
	
	def __unicode__(self):
		return u"%s %s" % (self.manager.first_name, self.manager.last_name)

class Timesheet(models.Model):
	user = models.ForeignKey(User)
	
	date = models.DateField(_('date'))
	time_in = models.TimeField(_('time in'))
	lunch_out = models.TimeField(_('lunch out'), blank=True, null=True)
	lunch_in = models.TimeField(_('lunch in'), blank=True, null=True)
	time_out = models.TimeField(_('time out'), blank=True, null=True)
	
	note = GenericRelation(Comment, object_id_field='object_pk')
	
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	class Meta:
		verbose_name = _('timesheet')
		verbose_name_plural = _('timesheets')
		db_table = 'timesheets'
		ordering = ('-date', 'date_modified')
		unique_together = (('user', 'date'))
	
	def __unicode__(self):
		return u"%s %s - %s" % (self.user.first_name, self.user.last_name, self.date)
	
	@property
	def lunch(self):
		if self.lunch_in and self.lunch_out:
			lunch = relativedelta(
				datetime.combine(self.date, self.lunch_in),
				datetime.combine(self.date, self.lunch_out)
			)
			
			return "%s.%s" % (lunch.hours, ((lunch.minutes * 100) / 60))
		elif self.lunch_out:
			lunch = relativedelta(
				datetime.now(),
				datetime.combine(self.date, self.lunch_out)
			)
			
			return "%s.%s" % (lunch.hours, ((lunch.minutes * 100) / 60))
		else:
			return 0
	
	@property
	def full_hours(self):
		if self.time_out:
			full_time = relativedelta(
				datetime.combine(self.date, self.time_out),
				datetime.combine(self.date, self.time_in)
			)
		else:
			full_time = relativedelta(
				datetime.now(),
				datetime.combine(self.date, self.time_in)
			)
		
		return "%s.%s" % (full_time.hours, ((full_time.minutes * 100) / 60))
	
	@property
	def hours(self):
		try:
			hours = float(self.full_hours) - float(self.lunch)
		except ValueError:
			hours = float(0)
		return hours
	
	@property
	def display_hours(self):
		if not self.hours == 0:
			return u"%s" % (self.hours)
		else:
			return 0