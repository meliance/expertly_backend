from rest_framework import serializers
from .models import ExpertDocument
from rest_framework.exceptions import ValidationError

class ExpertDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    expert_name = serializers.CharField(source='expert.user.username', read_only=True)

    class Meta:
        model = ExpertDocument
        fields = [
            'id', 'expert', 'expert_name', 'document_type', 'file', 'file_url',
            'version', 'title', 'description', 'is_verified', 'uploaded_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_url', 'version', 'uploaded_at', 'updated_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def validate_file(self, value):
        if value.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be less than 5MB.")
        if not value.name.lower().endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed.")
        return value