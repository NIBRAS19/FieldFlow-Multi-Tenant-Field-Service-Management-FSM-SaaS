from rest_framework import serializers
from .models import AuditLog
class AuditLogSerializer(serializers.ModelSerializer):
    actor_name=serializers.SerializerMethodField()
    class Meta: model=AuditLog; fields='__all__'
    def get_actor_name(self,obj): return obj.actor.get_full_name() if obj.actor else 'System'
