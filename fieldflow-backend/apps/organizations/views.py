from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Organization, Membership
from .serializers import OrganizationSerializer, MembershipSerializer
from .services import get_current_org, is_manager
from apps.accounts.models import User

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user, memberships__active=True).distinct()
    def perform_create(self, serializer):
        org = serializer.save(owner=self.request.user)
        Membership.objects.create(organization=org, user=self.request.user, role=User.Role.OWNER)
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        org = self.get_object()
        return Response(MembershipSerializer(org.memberships.select_related('user'), many=True).data)

class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all().select_related('user','organization')
    def get_queryset(self):
        org = get_current_org(self.request)
        return self.queryset.filter(organization=org)
    def perform_create(self, serializer):
        org = get_current_org(self.request)
        if not is_manager(self.request, org):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only managers can invite or manage members.')
        user_id = serializer.validated_data.pop('user_id')
        user = User.objects.get(pk=user_id)
        serializer.save(organization=org, user=user)
