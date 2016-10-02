'''
Created on Aug 29, 2016

@author: Dayo
'''
import sys

from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.apps import apps
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings

from .models import KITUser, KITUBalance, CoUserGroup

from sitegate.signals import sig_user_signup_success
from gomez.models import KITServicePlan
import arrow


@receiver(post_save, sender=KITUser)
def create_kituser_assoc_tables(sender, instance, **kwargs):
    if kwargs.get('created', False):
        def on_commit():
            kitbilling = apps.get_model('gomez', 'KITBilling')
            kitsystem = apps.get_model('gomez', 'KITSystem')
            
            kitbilling.objects.create(
                    kit_admin=instance,
                    next_due_date = timezone.now().date(),
                    registered_on = timezone.now().date()
                    )
            kitsystem.objects.create(kit_admin=instance)
            
            KITUBalance.objects.create(kit_user=instance)
            
        transaction.on_commit(on_commit) 

 
@receiver(post_save, sender=KITUser)
def create_and_set_default_user_group(sender, instance, *args, **kwargs):
    
    if instance.is_admin:
        
        #if not CoUserGroup.objects.filter(title='Default', kit_admin=instance).exists():
        
        kitadmin = KITUser.objects.get(pk=instance.id)
        
        try:
            coug, created = CoUserGroup.objects.get_or_create(
                    title = 'Default',
                    description = 'Default User Group',
                    kit_admin = kitadmin,
                    defaults = {
                        'active' : True
                                }
                )
            if created:
                instance.user_group = coug
        except:
            print("Error:", sys.exc_info())
            


@receiver(sig_user_signup_success)                
def free_trial_user_signup_callback(signup_result, flow, request, **kwargs):
    if request.path == '/register/free-trial/':
        #disconnect the post_save signal for KITUser
        post_save.disconnect(create_kituser_assoc_tables, sender=KITUser)
        
        # create new KITUser
        KITUser.objects.create(user=signup_result, is_admin=True)
        
        # connect again
        post_save.connect(create_kituser_assoc_tables, sender=KITUser)
        

        free_trial_service_plan = KITServicePlan.objects.get(id=settings.FREE_TRIAL_SERVICE_PLAN_ID)
        
        kitbilling = apps.get_model('gomez', 'KITBilling')
        kitbilling.objects.create(
                kit_admin=signup_result.kituser,
                service_plan = free_trial_service_plan,
                next_due_date = arrow.utcnow().replace(days=settings.FREE_TRIAL_VALIDITY_PERIOD).datetime.date(),
                registered_on = timezone.now().date(),
                account_status = 'AC'
                )
        
        kitsystem = apps.get_model('gomez', 'KITSystem')
        kitsystem.objects.create(kit_admin=signup_result.kituser)
        
        KITUBalance.objects.create(kit_user=signup_result.kituser, sms_balance=settings.FREE_TRIAL_FREE_SMS_UNITS)
        #set free user permissions
        group = Group.objects.get(id=settings.FREE_TRIAL_GROUP_PERMS_ID)
        signup_result.groups.add(group)
  