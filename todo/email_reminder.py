from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from todo.models import Task

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(skipped=False, due_date__gt=timezone.now())
    for task in tasks:
        reminder_datetime = task.due_date - timezone.timedelta(minutes=task.reminder_time)
        if reminder_datetime <= timezone.now():
            task_url = reverse('task-detail', kwargs={'pk': task.pk})
            message = f"Reminder: {task.title}\n\n{task.description}\n\nClick here to view task: {task_url}"
            send_mail(
                f"Reminder: {task.title}",
                message,
                "sender@example.com",
                [task.user.email],
                fail_silently=False,
            )

