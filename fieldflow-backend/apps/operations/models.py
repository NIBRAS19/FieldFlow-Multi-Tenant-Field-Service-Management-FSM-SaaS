from django.conf import settings
from django.db import models
from apps.organizations.models import Organization
from apps.customers.models import Customer, ServiceLocation, Asset

class ServiceType(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='service_types')
    name=models.CharField(max_length=120); description=models.TextField(blank=True); default_duration_minutes=models.PositiveIntegerField(default=60); active=models.BooleanField(default=True)
    def __str__(self): return self.name

class Technician(models.Model):
    class Status(models.TextChoices): AVAILABLE='available','Available'; EN_ROUTE='en_route','En Route'; ON_SITE='on_site','On Site'; OFFLINE='offline','Offline'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='technicians')
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='technician_profile')
    employee_code=models.CharField(max_length=60,blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.AVAILABLE)
    team=models.CharField(max_length=120,blank=True)
    area=models.CharField(max_length=120,blank=True)
    phone=models.CharField(max_length=40,blank=True)
    skills=models.JSONField(default=list,blank=True)
    certifications=models.JSONField(default=list,blank=True)
    utilization=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)

class ServiceRequest(models.Model):
    class Status(models.TextChoices): NEW='new','New'; IN_REVIEW='in_review','In Review'; APPROVED='approved','Approved'; REJECTED='rejected','Rejected'; CONVERTED='converted','Converted'
    class Priority(models.TextChoices): LOW='low','Low'; MEDIUM='medium','Medium'; HIGH='high','High'; URGENT='urgent','Urgent'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='service_requests')
    request_no=models.CharField(max_length=40)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='service_requests')
    location=models.ForeignKey(ServiceLocation,on_delete=models.SET_NULL,null=True,blank=True,related_name='service_requests')
    asset=models.ForeignKey(Asset,on_delete=models.SET_NULL,null=True,blank=True,related_name='service_requests')
    service_type=models.ForeignKey(ServiceType,on_delete=models.SET_NULL,null=True,blank=True)
    requester_name=models.CharField(max_length=180,blank=True)
    requester_phone=models.CharField(max_length=40,blank=True)
    title=models.CharField(max_length=220)
    description=models.TextField()
    priority=models.CharField(max_length=20,choices=Priority.choices,default=Priority.MEDIUM)
    preferred_date=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.NEW)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_service_requests')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']; constraints=[models.UniqueConstraint(fields=['organization','request_no'],name='uniq_request_org')]

class WorkOrder(models.Model):
    class Status(models.TextChoices): DRAFT='draft','Draft'; UNASSIGNED='unassigned','Unassigned'; SCHEDULED='scheduled','Scheduled'; ASSIGNED='assigned','Assigned'; EN_ROUTE='en_route','En Route'; ON_SITE='on_site','On Site'; IN_PROGRESS='in_progress','In Progress'; WAITING='waiting','Waiting'; COMPLETED='completed','Completed'; CANCELLED='cancelled','Cancelled'
    class Priority(models.TextChoices): LOW='low','Low'; MEDIUM='medium','Medium'; HIGH='high','High'; URGENT='urgent','Urgent'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='work_orders')
    work_order_no=models.CharField(max_length=40)
    request=models.OneToOneField(ServiceRequest,on_delete=models.SET_NULL,null=True,blank=True,related_name='work_order')
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='work_orders')
    location=models.ForeignKey(ServiceLocation,on_delete=models.SET_NULL,null=True,blank=True,related_name='work_orders')
    asset=models.ForeignKey(Asset,on_delete=models.SET_NULL,null=True,blank=True,related_name='work_orders')
    service_type=models.ForeignKey(ServiceType,on_delete=models.SET_NULL,null=True,blank=True,related_name='work_orders')
    title=models.CharField(max_length=220)
    description=models.TextField(blank=True)
    priority=models.CharField(max_length=20,choices=Priority.choices,default=Priority.MEDIUM)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.UNASSIGNED)
    scheduled_start=models.DateTimeField(null=True,blank=True); scheduled_end=models.DateTimeField(null=True,blank=True)
    estimated_minutes=models.PositiveIntegerField(default=60)
    actual_arrival=models.DateTimeField(null=True,blank=True); actual_start=models.DateTimeField(null=True,blank=True); actual_completed=models.DateTimeField(null=True,blank=True)
    sla_due_at=models.DateTimeField(null=True,blank=True)
    diagnosis=models.TextField(blank=True); completion_notes=models.TextField(blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_work_orders')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']; constraints=[models.UniqueConstraint(fields=['organization','work_order_no'],name='uniq_work_order_org')]

class WorkOrderAssignment(models.Model):
    work_order=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,related_name='assignments')
    technician=models.ForeignKey(Technician,on_delete=models.PROTECT,related_name='assignments')
    assigned_at=models.DateTimeField(auto_now_add=True); unassigned_at=models.DateTimeField(null=True,blank=True)
    is_primary=models.BooleanField(default=True)
    class Meta: ordering=['-assigned_at']

class ChecklistTemplate(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='checklist_templates')
    service_type=models.ForeignKey(ServiceType,on_delete=models.SET_NULL,null=True,blank=True,related_name='checklists')
    name=models.CharField(max_length=180); description=models.TextField(blank=True); active=models.BooleanField(default=True)

class ChecklistItem(models.Model):
    template=models.ForeignKey(ChecklistTemplate,on_delete=models.CASCADE,related_name='items')
    label=models.CharField(max_length=255); sort_order=models.PositiveIntegerField(default=0); required=models.BooleanField(default=False)

class WorkOrderChecklistItem(models.Model):
    work_order=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,related_name='checklist_items')
    label=models.CharField(max_length=255); sort_order=models.PositiveIntegerField(default=0); required=models.BooleanField(default=False)
    status=models.CharField(max_length=20,default='pending'); note=models.TextField(blank=True)

class Material(models.Model):
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='materials')
    sku=models.CharField(max_length=80); name=models.CharField(max_length=160); unit=models.CharField(max_length=40,default='piece'); unit_cost=models.DecimalField(max_digits=12,decimal_places=2,default=0); stock_quantity=models.DecimalField(max_digits=12,decimal_places=2,default=0); active=models.BooleanField(default=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['organization','sku'],name='uniq_material_org')]

class WorkOrderMaterial(models.Model):
    work_order=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,related_name='materials')
    material=models.ForeignKey(Material,on_delete=models.PROTECT)
    quantity=models.DecimalField(max_digits=12,decimal_places=2); unit_cost=models.DecimalField(max_digits=12,decimal_places=2)
    @property
    def total(self): return self.quantity*self.unit_cost

class Attachment(models.Model):
    work_order=models.ForeignKey(WorkOrder,on_delete=models.CASCADE,related_name='attachments')
    file=models.FileField(upload_to='work-orders/%Y/%m/%d/')
    kind=models.CharField(max_length=30,default='photo')
    caption=models.CharField(max_length=255,blank=True)
    uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)

class CustomerSignature(models.Model):
    work_order=models.OneToOneField(WorkOrder,on_delete=models.CASCADE,related_name='signature')
    customer_name=models.CharField(max_length=180)
    signature_data=models.TextField()
    signed_at=models.DateTimeField(auto_now_add=True)
    ip_address=models.GenericIPAddressField(null=True,blank=True)

class Notification(models.Model):
    class Type(models.TextChoices): INFO='info','Info'; SUCCESS='success','Success'; WARNING='warning','Warning'; ERROR='error','Error'
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='notifications')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    title=models.CharField(max_length=180); message=models.TextField(); type=models.CharField(max_length=20,choices=Type.choices,default=Type.INFO); read=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)

class ActivityLogBase(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: abstract=True
