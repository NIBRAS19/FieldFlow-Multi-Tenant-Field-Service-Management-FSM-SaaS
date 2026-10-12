from django.utils import timezone
from .models import WorkOrder, WorkOrderAssignment, Technician, WorkOrderChecklistItem, CustomerSignature, Attachment, Notification
from apps.audit.models import AuditLog

def next_number(model, field, prefix, organization):
    last = model.objects.filter(organization=organization).order_by('-id').values_list(field, flat=True).first()
    number = 1
    if last:
        try: number = int(str(last).split('-')[-1]) + 1
        except Exception: number = model.objects.filter(organization=organization).count() + 1
    return f'{prefix}-{number:04d}'

def audit(user, org, action, resource, resource_id, before=None, after=None):
    AuditLog.objects.create(actor=user, organization=org, action=action, resource=resource, resource_id=str(resource_id), before=before or {}, after=after or {})

def assign_technician(work_order, technician, user):
    WorkOrderAssignment.objects.filter(work_order=work_order, unassigned_at__isnull=True).update(unassigned_at=timezone.now())
    WorkOrderAssignment.objects.create(work_order=work_order, technician=technician, is_primary=True)
    work_order.status = WorkOrder.Status.ASSIGNED if not work_order.scheduled_start else WorkOrder.Status.SCHEDULED
    work_order.save(update_fields=['status','updated_at'])
    technician.status = Technician.Status.AVAILABLE
    technician.save(update_fields=['status'])
    audit(user, work_order.organization, 'assign_technician', 'work_order', work_order.id, after={'technician_id': technician.id})

def transition(work_order, new_status, user):
    old = work_order.status
    work_order.status = new_status
    now=timezone.now()
    if new_status == WorkOrder.Status.ON_SITE: work_order.actual_arrival=now
    if new_status == WorkOrder.Status.IN_PROGRESS: work_order.actual_start=now
    if new_status == WorkOrder.Status.COMPLETED: work_order.actual_completed=now
    work_order.save(update_fields=['status','actual_arrival','actual_start','actual_completed','updated_at'])
    audit(user, work_order.organization, 'status_change', 'work_order', work_order.id, before={'status':old}, after={'status':new_status})

def notify(org, user, title, message, type='info'):
    return Notification.objects.create(organization=org,user=user,title=title,message=message,type=type)
