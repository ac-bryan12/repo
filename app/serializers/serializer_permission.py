from django.contrib.auth.models import Group,Permission
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)

    class Meta:
        model=Group
        fields = ['name']

class PermissionSerializer(serializers.ModelSerializer):
    codename = serializers.CharField(max_length=100)

    class Meta:
        model=Permission
        fields = ['codename']