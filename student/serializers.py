from rest_framework import serializers

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
