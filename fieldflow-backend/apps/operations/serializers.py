from rest_framework import serializers
from .models import *

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta: model=ServiceType; fields='__all__'; read_only_fields=['organization']
class TechnicianSerializer(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    class Meta: model=Technician; fields='__all__'; read_only_fields=['organization']
    def get_user_name(self,obj): return obj.user.get_full_name() or obj.user.username
class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta: model=ServiceRequest; fields='__all__'; read_only_fields=['organization','request_no','created_by']
class WorkOrderAssignmentSerializer(serializers.ModelSerializer):
    technician_name=serializers.CharField(source='technician.user.get_full_name',read_only=True)
    class Meta: model=WorkOrderAssignment; fields=['id','work_order','technician','technician_name','assigned_at','unassigned_at','is_primary']; read_only_fields=['assigned_at','unassigned_at']
class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta: model=ChecklistItem; fields='__all__'
class ChecklistTemplateSerializer(serializers.ModelSerializer):
    items=ChecklistItemSerializer(many=True,required=False)
    class Meta: model=ChecklistTemplate; fields=['id','organization','service_type','name','description','active','items']; read_only_fields=['organization']
    def create(self, validated_data):
        items=validated_data.pop('items',[]); obj=ChecklistTemplate.objects.create(**validated_data)
        ChecklistItem.objects.bulk_create([ChecklistItem(template=obj,**i) for i in items]); return obj
class WorkOrderChecklistSerializer(serializers.ModelSerializer):
    class Meta: model=WorkOrderChecklistItem; fields='__all__'; read_only_fields=['work_order']
class MaterialSerializer(serializers.ModelSerializer):
    class Meta: model=Material; fields='__all__'; read_only_fields=['organization']
class WorkOrderMaterialSerializer(serializers.ModelSerializer):
    total=serializers.DecimalField(max_digits=14,decimal_places=2,read_only=True)
    class Meta: model=WorkOrderMaterial; fields=['id','work_order','material','quantity','unit_cost','total']
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta: model=Attachment; fields='__all__'; read_only_fields=['uploaded_by']
class SignatureSerializer(serializers.ModelSerializer):
    class Meta: model=CustomerSignature; fields='__all__'; read_only_fields=['signed_at','ip_address']
class WorkOrderSerializer(serializers.ModelSerializer):
    assignments=WorkOrderAssignmentSerializer(many=True,read_only=True)
    checklist_items=WorkOrderChecklistSerializer(many=True,read_only=True)
    materials=WorkOrderMaterialSerializer(many=True,read_only=True)
    attachments=AttachmentSerializer(many=True,read_only=True)
    signature=SignatureSerializer(read_only=True)
    class Meta: model=WorkOrder; fields='__all__'; read_only_fields=['organization','work_order_no','created_by','actual_arrival','actual_start','actual_completed']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta: model=Notification; fields='__all__'; read_only_fields=['organization','user']
