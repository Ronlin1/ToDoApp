import datetime
from django.utils import timezone
from todo.models import Task

def mark_tasks_as_skipped():
    now = timezone.now()
    # print(now)
    Task.objects.filter(complete=False, due_date__lt=now).update(skipped=True)
