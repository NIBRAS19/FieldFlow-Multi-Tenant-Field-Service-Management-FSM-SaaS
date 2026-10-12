from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','phone','role','timezone','avatar','is_active']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    organization_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','phone','organization_name']

    def create(self, validated_data):
        org_name = validated_data.pop('organization_name')
        from apps.organizations.models import Organization, Membership
        user = User.objects.create_user(**validated_data, role=User.Role.OWNER)
        org = Organization.objects.create(name=org_name, owner=user)
        Membership.objects.create(organization=org, user=user, role=User.Role.OWNER)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user or not user.is_active:
            raise serializers.ValidationError('Invalid username or password.')
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': UserSerializer(user).data}
