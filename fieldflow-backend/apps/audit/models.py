from django.conf import settings
from django.db import models
from apps.organizations.models import Organization

class AuditLog(models.Model):
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='audit_events')
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='audit_logs')
    action=models.CharField(max_length=120)
    resource=models.CharField(max_length=120)
    resource_id=models.CharField(max_length=80)
    before=models.JSONField(default=dict,blank=True)
    after=models.JSONField(default=dict,blank=True)
    ip_address=models.GenericIPAddressField(null=True,blank=True)
    user_agent=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
