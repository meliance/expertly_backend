from rest_framework import serializers
from accounts.models import Expert  # Adjust the import based on your model location

class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = '__all__'