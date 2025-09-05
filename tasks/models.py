from django.db import models
from django.conf import settings

class TaskManager(models.Manager):
    def completed_last_n_days(self, days=7):
        from django.utils import timezone
        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(status='completed', updated_at__gte=since)

class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)  # <-- Add this line
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title