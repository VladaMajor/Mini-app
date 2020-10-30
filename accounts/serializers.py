from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdditionalUserData, Permissions, Permission_type

class PermissionsTypeSeriallizer(serializers.ModelSerializer):

    class Meta:
        model = Permission_type
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class PermissionsSeriallizer(serializers.ModelSerializer):
    fk_account = UserSerializer()
    fk_permission_type = PermissionsTypeSeriallizer()

    class Meta:
        model = Permissions
        fields = '__all__'
