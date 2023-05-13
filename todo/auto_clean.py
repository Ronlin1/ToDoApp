from todo.models import Task

from celery import shared_task
from datetime import timedelta
from django.utils import timezone

@shared_task
def cleanup_tasks():
    threshold_date = timezone.now() - timedelta(days=7)
    Task.objects.filter(created_at__lt=threshold_date).delete()
