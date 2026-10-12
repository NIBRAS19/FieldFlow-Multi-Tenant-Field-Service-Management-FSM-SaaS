from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization,Membership
from apps.customers.models import Customer,ServiceLocation,Asset
from apps.operations.models import ServiceType,Technician,ServiceRequest,WorkOrder,ChecklistTemplate,ChecklistItem,Material
from apps.invoices.models import Invoice,InvoiceItem
from apps.invoices.services import next_invoice_no,recalc
from django.utils import timezone
from datetime import timedelta

User=get_user_model()
class Command(BaseCommand):
    help='Create a complete FieldFlow demo workspace.'
    def handle(self,*args,**kwargs):
        user,created=User.objects.get_or_create(username='nibras',defaults={'first_name':'Nibras','last_name':'Demo','email':'nibras@example.com','role':'owner','is_staff':True,'is_superuser':True})
        user.is_staff = True
        user.is_superuser = True
        if created: user.set_password('FieldFlow123!')
        user.save()
        org,_=Organization.objects.get_or_create(name='FieldFlow Demo',defaults={'owner':user,'industry':'Facilities Management','country':'United Arab Emirates','currency':'AED'})
        Membership.objects.get_or_create(organization=org,user=user,defaults={'role':'owner'})
        for first,last,email,role in [('Ahmed','Hassan','ahmed@fieldflow.local','technician'),('Sara','Ali','sara@fieldflow.local','technician'),('Omar','Khan','omar@fieldflow.local','technician'),('Lina','Joseph','lina@fieldflow.local','technician')]:
            u,_=User.objects.get_or_create(username=email.split('@')[0],defaults={'first_name':first,'last_name':last,'email':email,'role':role}); u.set_password('FieldFlow123!'); u.save()
            Membership.objects.get_or_create(organization=org,user=u,defaults={'role':role})
            Technician.objects.get_or_create(organization=org,user=u,defaults={'employee_code':first[:2].upper()+'001','area':'Abu Dhabi'})
        services=[]
        for name in ['AC Maintenance','Electrical Inspection','Plumbing Repair','HVAC Service','Equipment Check']:
            services.append(ServiceType.objects.get_or_create(organization=org,name=name,defaults={'default_duration_minutes':90})[0])
        customers=[]
        for company,contact,phone in [('ABC Trading LLC','Mariam Rahman','+971501234456'),('Nexa Facilities','Faisal Noor','+971553341182'),('Greenline Cafe','Aisha Ali','+971527642201'),('Vertex Clinic','Omar Saeed','+971562106789'),('Nova Retail','Ryan George','+971503401143')]:
            customers.append(Customer.objects.get_or_create(organization=org,company=company,defaults={'name':company,'contact_name':contact,'phone':phone})[0])
        locs=[]
        for c,name in zip(customers,['Office Building A','Warehouse 3','Al Khalidiyah','Muroor Branch','Reem Mall']):
            locs.append(ServiceLocation.objects.get_or_create(organization=org,customer=c,name=name,defaults={'address_line':name+', Abu Dhabi','city':'Abu Dhabi'})[0])
        req_specs=[('AC not cooling','high',customers[3],locs[3],services[0]),('Sink leaking under counter','urgent',customers[2],locs[2],services[2]),('Quarterly AC maintenance','medium',customers[0],locs[0],services[0]),('Freezer temperature alarm','high',customers[4],locs[4],services[4])]
        for title,priority,c,l,s in req_specs:
            if not ServiceRequest.objects.filter(organization=org,title=title).exists():
                ServiceRequest.objects.create(organization=org,request_no=f'REQ-{1100+ServiceRequest.objects.filter(organization=org).count():04d}',customer=c,location=l,service_type=s,title=title,description=title,priority=priority,created_by=user)
        for c,l,s in [(customers[0],locs[0],services[0]),(customers[1],locs[1],services[1]),(customers[2],locs[2],services[2]),(customers[3],locs[3],services[0]),(customers[4],locs[4],services[4])]:
            if not WorkOrder.objects.filter(organization=org,customer=c,title=s.name).exists():
                WorkOrder.objects.create(organization=org,work_order_no=f'WO-{1045+WorkOrder.objects.filter(organization=org).count():04d}',customer=c,location=l,service_type=s,title=s.name,description='Demo service work order',priority='high' if c==customers[0] else 'medium',status='scheduled',scheduled_start=timezone.now()+timedelta(hours=1),scheduled_end=timezone.now()+timedelta(hours=2),created_by=user)
        if not Material.objects.filter(organization=org).exists(): Material.objects.create(organization=org,sku='FILTER-001',name='AC Filter',unit='piece',unit_cost=75,stock_quantity=100)
        self.stdout.write(self.style.SUCCESS('Demo workspace ready. Username: nibras / Password: FieldFlow123!'))
