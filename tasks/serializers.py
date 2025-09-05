from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "created_at", "updated_at"]

    def create(self, validated_data):
        # Don't add owner here, it's already passed in the view
        return Task.objects.create(**validated_data)
