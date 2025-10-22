# strings/serializers.py
from rest_framework import serializers

class CreateStringSerializer(serializers.Serializer):
    value = serializers.CharField()

class StoredStringSerializer(serializers.Serializer):
    id = serializers.CharField()
    value = serializers.CharField()
    properties = serializers.DictField()
    created_at = serializers.DateTimeField()
