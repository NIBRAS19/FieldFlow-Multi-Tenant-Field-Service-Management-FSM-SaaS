from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.views import LoginView, MeView, RegisterView
from apps.organizations.views import OrganizationViewSet, MembershipViewSet
from apps.customers.views import CustomerViewSet, ServiceLocationViewSet, AssetViewSet
from apps.operations.views import (
    ServiceTypeViewSet, TechnicianViewSet, ServiceRequestViewSet,
    WorkOrderViewSet, ChecklistTemplateViewSet, MaterialViewSet,
    NotificationViewSet, DashboardView, DispatchView, TechnicianTodayView,
)
from apps.invoices.views import InvoiceViewSet
from apps.audit.views import AuditLogViewSet

router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organization')
router.register('memberships', MembershipViewSet, basename='membership')
router.register('customers', CustomerViewSet, basename='customer')
router.register('locations', ServiceLocationViewSet, basename='location')
router.register('assets', AssetViewSet, basename='asset')
router.register('service-types', ServiceTypeViewSet, basename='service-type')
router.register('technicians', TechnicianViewSet, basename='technician')
router.register('requests', ServiceRequestViewSet, basename='request')
router.register('work-orders', WorkOrderViewSet, basename='work-order')
router.register('checklists', ChecklistTemplateViewSet, basename='checklist')
router.register('materials', MaterialViewSet, basename='material')
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/register/', RegisterView.as_view()),
    path('api/v1/auth/login/', LoginView.as_view()),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view()),
    path('api/v1/auth/me/', MeView.as_view()),
    path('api/v1/dashboard/', DashboardView.as_view()),
    path('api/v1/dispatch/', DispatchView.as_view()),
    path('api/v1/technician/today/', TechnicianTodayView.as_view()),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
