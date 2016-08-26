from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields.jsonb import JSONField
import uuid

# Create your models here.



class SMSDeliveryReport(models.Model):
    
    STATUS = (
        (0, 'ACCEPTED'),
        (1, 'PENDING'),
        (2, 'UNDELIVERABLE'),
        (3, 'DELIVERED'),
        (4, 'EXPIRED'),
        (5, 'REJECTED')
              )
    
    ERROR = (
        (0, 'OK'),
        (1, 'HANDSET_ERROR'),
        (2, 'USER_ERROR'),
        (3, 'OPERATOR_ERROR')
             )

    MSG_ORIGIN = (
        (0, 'Transactional'),
        (1, 'Bulk SMS'),
                  )

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_id = models.UUIDField(db_index=True, editable=False, help_text="A.K.A Process ID or Bulk ID")
    origin = models.CharField(max_length=1, choices=MSG_ORIGIN)
    
    to_phone = PhoneNumberField(blank=False)
    sms_message = JSONField()
    sms_gateway = JSONField()
    
    msg_status = models.CharField(max_length=20, choices=STATUS)
    msg_error = models.CharField(max_length=20, choices=ERROR)
    
    kituser_id = models.IntegerField(db_index=True)
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "SMS to {}".format(self.to_phone.as_international)
    

class SMSDeliveryReportHistory(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.ForeignKey(SMSDeliveryReport, on_delete=models.CASCADE)
    data = JSONField()
    
    
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
    
    