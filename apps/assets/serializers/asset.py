# -*- coding: utf-8 -*-
#
from rest_framework import serializers
from rest_framework_bulk.serializers import BulkListSerializer

from common.mixins import BulkSerializerMixin
from ..models import Asset
from .system_user import AssetSystemUserSerializer

__all__ = [
    'AssetSerializer', 'AssetGrantedSerializer', 'MyAssetGrantedSerializer',
    'AssetAsNodeSerializer', 'AssetSimpleSerializer', 'AssetExportSerializer',
    'AssetImportTemplateSerializer'
]


class AssetSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Asset
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        validators = []

    @classmethod
    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('labels', 'nodes')\
            .select_related('admin_user')
        return queryset

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend([
            'hardware_info', 'connectivity', 'org_name'
        ])
        return fields


class AssetAsNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'hostname', 'ip', 'port', 'platform', 'protocol']


class AssetGrantedSerializer(serializers.ModelSerializer):
    """
    被授权资产的数据结构
    """
    system_users_granted = AssetSystemUserSerializer(many=True, read_only=True)
    system_users_join = serializers.SerializerMethodField()
    # nodes = NodeTMPSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = (
            "id", "hostname", "ip", "port", "system_users_granted",
            "is_active", "system_users_join", "os", 'domain',
            "platform", "comment", "protocol", "org_id", "org_name",
        )

    @staticmethod
    def get_system_users_join(obj):
        system_users = [s.username for s in obj.system_users_granted]
        return ', '.join(system_users)


class MyAssetGrantedSerializer(AssetGrantedSerializer):
    """
    普通用户获取授权的资产定义的数据结构
    """

    class Meta:
        model = Asset
        fields = (
            "id", "hostname", "system_users_granted",
            "is_active", "system_users_join", "org_name",
            "os", "platform", "comment", "org_id", "protocol"
        )


class AssetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'hostname', 'port', 'ip', 'connectivity']


class AssetExportSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    admin_user = serializers.SerializerMethodField()

    @staticmethod
    def get_admin_user(obj):
        return obj.admin_user

    class Meta:
        model = Asset
        fields = [
            'id', 'ip', 'hostname', 'protocol', 'port', 'platform', 'domain',
            'is_active', 'admin_user', 'public_ip', 'number', 'vendor', 'model',
            'sn', 'cpu_model', 'cpu_count', 'cpu_cores', 'cpu_vcpus', 'memory',
            'disk_total', 'disk_info', 'os', 'os_version', 'os_arch',
            'hostname_raw', 'created_by', 'comment'
        ]


class AssetImportTemplateSerializer(AssetExportSerializer):
    class Meta:
        model = Asset
        fields = [
            'id', 'ip', 'hostname', 'protocol', 'port', 'platform', 'domain',
            'is_active', 'admin_user', 'public_ip',
        ]
