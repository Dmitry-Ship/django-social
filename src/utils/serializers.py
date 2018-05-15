from rest_framework import serializers
from entities.serializers import EntitySerializer


class TargetAsIdSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    @staticmethod
    def get_id(obj):
        return EntitySerializer(obj.id).data['id']