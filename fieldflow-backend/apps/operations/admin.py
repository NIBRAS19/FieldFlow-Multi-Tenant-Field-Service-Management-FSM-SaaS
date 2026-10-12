from django.contrib import admin
from .models import *
admin.site.register([ServiceType,Technician,ServiceRequest,WorkOrder,WorkOrderAssignment,ChecklistTemplate,ChecklistItem,WorkOrderChecklistItem,Material,WorkOrderMaterial,Attachment,CustomerSignature,Notification])
