import sys
import datetime
import html2text
import uuid
from dateutil.relativedelta import relativedelta
from dateutil.parser import *

from django.db import models, transaction
from django.apps import apps
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from phonenumber_field.modelfields import PhoneNumberField
import arrow
from picklefield.fields import PickledObjectField


def get_default_time():
    # default delivery time
    return timezone.now()+datetime.timedelta(seconds=settings.MSG_WAIT_TIME)

class StandardMessaging(models.Model):
    
    STATUS = Choices('draft', 'waiting', 'processed')
    
    title = models.CharField(max_length=100, blank=False)
    email_message = models.TextField(blank=True)
    sms_message = models.TextField(blank=True)
    
    send_sms = models.BooleanField(verbose_name="Send SMS")
    insert_optout = models.BooleanField(verbose_name = "Insert Unsubscribe")
    
    send_email = models.BooleanField(verbose_name="Send Email")
    recipients = models.ManyToManyField('core.Contact', related_name="recipients")
    
    ###
    copied_recipients = models.ManyToManyField('core.Contact', related_name="cc_recipients", blank=True,\
                                               help_text = "Contacts selected in this field will receive a copy of the messages sent to Recipients")
    
    cc_recipients_send_sms = models.BooleanField(verbose_name="Send SMS", default=True)
    cc_recipients_send_email = models.BooleanField(verbose_name="Send Email", default=True)
    ###
    
    delivery_time = models.DateTimeField(default=get_default_time, verbose_name = "Deliver at")
    
    smtp_setting = models.ForeignKey('core.SMTPSetting', null=True, blank=True, verbose_name="SMTP Account")
    sms_sender = models.CharField(max_length=11, blank=True, verbose_name="SMS Sender")
    
    
    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    status = StatusField()
    #waiting_at = MonitorField(monitor='status', when=['waiting'])
    #processed_at = MonitorField(monitor='status', when=['processed'])
    

    def __str__(self):
        if self.send_sms:
            sms_m = self.sms_message
            length = 75
            return ("S: {}...".format(sms_m[0:length]) if len(sms_m) > length else "{}".format(sms_m))
        elif self.send_email:
            email_m = html2text.html2text(self.email_message)
            length = 90
            return "{}...".format(email_m[0:length]) if len(email_m) > length else "{}".format(email_m)
            
            
    
    def get_absolute_url(self):
        return reverse('messaging:standard-message-draft',args=[self.pk])
    
    
    class Meta:
        verbose_name_plural = "Standard Messaging"
    
    
class AdvancedMessaging(models.Model):
    
    STATUS = Choices('draft', 'waiting', 'processed')
    
        
    REPEAT = (
        ("norepeat",_("No Repeat")),
        ("hourly",_("Hourly")),
        ("daily",_("Daily")),
        ("weekly",_("Weekly")),
        ("monthly",_("Monthly")),
        ("quarterly",_("Quarterly")),
        ("annually",_("Annually")),
              )
    
    title = models.CharField(max_length=100, blank=False)
    message_template = models.ForeignKey('core.MessageTemplate', blank=False)
    
    contact_group = models.ManyToManyField('core.ContactGroup', verbose_name = "Contact List")
    custom_data_namespace = models.ForeignKey('core.CustomData', on_delete=models.PROTECT, null=True, blank=True)
    
    delivery_time = models.DateTimeField(default=get_default_time, verbose_name = "Deliver at")
    repeat_frequency = models.CharField(max_length=20, choices=REPEAT, default="norepeat")
    repeat_until = models.DateTimeField(blank=True, null=True)
    
    next_event = models.DateTimeField()
       
    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    
    status = StatusField()
    #waiting_at = MonitorField(monitor='status', when=['waiting'])
    #processed_at = MonitorField(monitor='status', when=['processed'])
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
            
    def get_absolute_url(self):
        return reverse('messaging:advanced-message-draft',args=[self.pk])
    
    def _next_event_time(self):
        if self.repeat_frequency == "norepeat":
            return self.delivery_time
        elif self.repeat_frequency == "hourly":
            return self.delivery_time+relativedelta(hours=1)
        elif self.repeat_frequency == "daily":
            return self.delivery_time+relativedelta(days=1)
        elif self.repeat_frequency == "weekly":
            return self.delivery_time+relativedelta(weeks=1)
        elif self.repeat_frequency == "monthly":
            return self.delivery_time+relativedelta(months=1)
        elif self.repeat_frequency == "quarterly":
            return self.delivery_time+relativedelta(months=3)
        elif self.repeat_frequency == "annually":
            return self.delivery_time+relativedelta(years=1)   
        
    
    def save(self, *args, **kwargs):
        #self.next_event = self._next_event_time()
        self.next_event = self.delivery_time
        super(AdvancedMessaging, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Advanced Messaging"
        
    

class QueuedMessages(models.Model):
    
    MSG_TYPE = (
        ('ADVANCED',' Advanced'),
        ('STANDARD',' Standard')
                )
    
    message_type = models.CharField(max_length=10, choices=MSG_TYPE)
    message_id = models.PositiveIntegerField()   
    message = JSONField() #message, recipients
    delivery_time = models.DateTimeField(default=get_default_time, verbose_name = "Deliver at")
    recurring = models.BooleanField(default=False)
    
    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    queued_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} Message {}".format(self.message_type,self.message_id)
    
    def get_absolute_url(self):
        return None
    
    class Meta:
        verbose_name_plural = "Queued Messages"


class ProcessedMessages(models.Model):
    
    MSG_TYPE = (
        ('ADVANCED',' Advanced'),
        ('STANDARD',' Standard'),
        ('REMINDER',' Reminder'),
                )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_type = models.CharField(max_length=10, choices=MSG_TYPE)
    message = JSONField() #template, recipient_ids

    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    #status = models.CharField(max_length=30)
    
    def __str__(self):
        return "{} by {}".format(self.message_type, self.created_by)
    
    def get_absolute_url(self):
        return None
    
    class Meta:
        verbose_name_plural = "Processed Messages"
        

def event_date(period, value, date_text, direction):
    # @params dir:direction
    print(date_text)
    
    try:
        
        usedate = parse(date_text)
        
        if direction == "before":
            if period == "day":
                return arrow.get(usedate).replace(days=-value).datetime
            elif period == "week":
                return arrow.get(usedate).replace(weeks=-value).datetime
            elif period == "month":
                return arrow.get(usedate).replace(months=-value).datetime
            elif period == "year":
                return arrow.get(usedate).replace(years=-value).datetime
        elif direction == "after":
            if period == "day":
                return arrow.get(usedate).replace(days=+value).datetime
            elif period == "week":
                return arrow.get(usedate).replace(weeks=+value).datetime
            elif period == "month":
                return arrow.get(usedate).replace(months=+value).datetime
            elif period == "year":
                return arrow.get(usedate).replace(years=+value).datetime
    except:
        print(sys.exc_info())

         
                
                
class RunningMessage(models.Model):
    
    message = JSONField()
    contact_dsoi = JSONField() #[["X27NC6XGP", "15/8/2017"],["V27NC6XGS", "5/2/2017"]]
    reminders = JSONField() # [[2, "week", "before"], [5, "day", "after"]]
    last_event_on = models.DateTimeField()
    completed = models.BooleanField(default=False)
    
    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    started_at = models.DateTimeField(auto_now_add=True)
    
    def set_is_completed(self):
        if self.reminders is None:
            self.completed = True
    
    def get_events_due_within_the_next_day(self):
        # is date between now and next 1 hour?
        # store in a to_be_processed_table, else proceed
        
        due_events=[]
        
        for reminder in self.reminders:
            for dsoi in self.contact_dsoi:
                
                focal_date = event_date(reminder[1],reminder[0],dsoi[1],reminder[2])
                if arrow.utcnow().floor('day') <= focal_date  <=  arrow.utcnow().ceil('day'):
                    due_events.append([self.message,dsoi[0], dsoi[1], reminder, self.created_by]) 
        
        # check if there are any more events, if not, mark as completed            
        if self.last_event_on <= arrow.utcnow().ceil('day'):
            self.completed = True #setting completed shunts the entire function
            self.save()
        
        return due_events
        
        
    def __str__(self):
        return self.message["title"]
    

    
    
class ReminderMessaging(models.Model):
    
    
    STATUS = Choices('draft', 'running', 'completed')
    
    title = models.CharField(max_length=100, blank=False)
    message_template = models.ForeignKey('core.MessageTemplate', blank=False)
    contact_group = models.ManyToManyField('core.ContactGroup')    
    
    custom_data_namespace = models.ForeignKey('core.CustomData', on_delete=models.PROTECT)
    date_column = models.CharField(max_length=500)
       
    created_by = models.ForeignKey('core.KITUser', models.PROTECT)
    
    is_active = models.BooleanField(default=True)
    status = StatusField()
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_custom_data_header_selected_choices(self):
        #choices and selected for the use in form
        if self.custom_data_namespace:
            
            chs = []
            hdrs = self.custom_data_namespace.headers
            
            # remove identity fields from selectable
            hdrs.remove(self.custom_data_namespace.identity_column_name)
            
            for header_item in hdrs:
                chs.append((header_item, header_item))
            
            headers = tuple(chs)
            return [headers,self.date_column]
        else:
            return []
            
    def get_absolute_url(self):
        return reverse('messaging:reminder-message-draft',args=[self.pk])  
        
    
    def save(self, *args, **kwargs):
        super(ReminderMessaging, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Reminder Messaging"


class Reminder(models.Model):
    
    DELTA = (
        ("day",_("Days")),
        ("week",_("Weeks")),
        ("month",_("Months")),
        ("year",_("Years")),
              )
    DELTADIR = (
        ('before', _("Before")),
        ('after', _("After"))
                )
    
    message = models.ForeignKey(ReminderMessaging, on_delete=models.CASCADE)
    delta_value = models.PositiveSmallIntegerField(blank=False)
    delta_type = models.CharField(max_length=20, choices=DELTA, default="day", blank=False)
    delta_direction = models.CharField(max_length=10, choices=DELTADIR, default="before", blank=False)
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}, {} {} {}".format(self.message, self.delta_value, self.delta_type, self.delta_direction)



    
class IssueFeedback(models.Model):
    title = models.CharField(max_length=150, blank=False)
    detail = models.TextField(blank=False)
    screenshot = models.ImageField(upload_to="issue_feedback/", blank=True)
    
    resolution_flag = models.BooleanField(default=False)
    
    submitter = models.ForeignKey('core.KITUser', on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class FailedKITMessage(models.Model):
    
    mcat = (
        ('running_msg', 'Running'),
        ('queued_msg', 'Queued'),
        ('private_anniv_msg', 'Private Anniv.'),
        ('public_anniv_msg', 'Public Anniv.'),
            )
    
    message_data = PickledObjectField()
    message_category = models.CharField(max_length=20, choices=mcat)
    reason = models.CharField(max_length=255)
    retries = models.PositiveSmallIntegerField(default=0)
    
    owned_by = models.ForeignKey('core.KITUser', on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} Message Failed at {}".format(self.message_category, self.created)
    
    def get_absolute_url(self):
        return reverse('messaging:failed-kit-message-retry',args=[self.pk])
    
    class Meta:
        verbose_name = "Failed Message"
    
    

class FailedSMSMessage(models.Model):
    
    sms_pickled_data = PickledObjectField()
    reason = models.CharField(max_length=255)
    retries = models.PositiveSmallIntegerField(default=0)
    batch_id = models.CharField(max_length=100, default='')
    
    owned_by = models.ForeignKey('core.KITUser', on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "SMS Failed at {}".format(self.created)
    
    def get_absolute_url(self):
        return reverse('messaging:failed-sms-message-retry',args=[self.pk])
    
    

class FailedEmailMessage(models.Model):
    
    email_pickled_data = PickledObjectField()
    reason = models.CharField(max_length=255)
    retries = models.PositiveSmallIntegerField(default=0)
    
    owned_by = models.ForeignKey('core.KITUser', on_delete=models.SET_NULL, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Email Failed at {}".format(self.created)
    
    def get_absolute_url(self):
        return reverse('messaging:failed-email-message-retry',args=[self.pk])


########### System Model #################   
    
class FailedSMSSystemBacklog(models.Model):
    sms_pickled_data = PickledObjectField()
    reason = models.CharField(max_length=255)    
    owned_by = models.ForeignKey('core.KITUser', on_delete=models.SET_NULL, null=True)
    batch_id = models.CharField(max_length=100, default='')
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "SMS Failed at {}".format(self.created)
    
    def get_absolute_url(self):
        return None
    