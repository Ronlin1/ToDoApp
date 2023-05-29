from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from todo.models import Task
from django.shortcuts import render
from django.utils import timezone


def send_reminder_email(user_id, task_id, reminder_time):
    user = User.objects.get(pk=user_id)
    task = Task.objects.get(pk=task_id)
    subject = f'Reminder: Task "{task.title}" due soon'
    message = render_to_string('todo/email_reminder.html', {
        'user': user,
        'task': task,
        'reminder_time': reminder_time
    })
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print("-1-1-")

def auto_send():
    # print(timezone.now())
    for task in Task.objects.all():
        due_date = timezone.localtime(task.due_date)
        reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)
        print(timezone.now(), "TZ")
        print(reminder_time ,"RT")
        try:
            if timezone.now() == reminder_time:
                # Send the reminder email
                send_reminder_email(task.user.pk, task.pk, reminder_time)
        except Exception as e:print(e)
    
    
