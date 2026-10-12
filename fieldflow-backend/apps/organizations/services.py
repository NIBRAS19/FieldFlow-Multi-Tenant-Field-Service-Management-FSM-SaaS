from rest_framework.exceptions import ValidationError
from .models import Organization, Membership

def get_current_org(request, required=True):
    raw = request.headers.get('X-Organization-ID') or request.query_params.get('organization') or request.data.get('organization')
    memberships = Membership.objects.filter(user=request.user, active=True).select_related('organization')
    if raw:
        try:
            org = memberships.get(organization_id=raw).organization
        except Membership.DoesNotExist:
            raise ValidationError('You do not have access to this organization.')
    else:
        first = memberships.first()
        if not first:
            if required:
                raise ValidationError('No active organization membership.')
            return None
        org = first.organization
    return org

def is_manager(request, organization):
    return Membership.objects.filter(organization=organization, user=request.user, active=True, role__in=['owner','admin','operations','dispatcher','finance']).exists()
