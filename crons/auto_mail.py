from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from todo.models import Task
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage


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

    # Create an instance of `EmailMessage` 
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = "html"
    email.send()

    # Print the HTML message
    # print(message)
    print("EMAIL SENT---------")

def auto_send():
    for task in Task.objects.all():
        due_date = timezone.localtime(task.due_date)
        reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)
        reminder_time = reminder_time.replace(tzinfo=None) # remove timezone offset
        current_time = timezone.now() + timedelta(hours=3) # add 3 hours to current time
        reminder_time_str = reminder_time.strftime('%Y-%m-%d %H:%M:%S') # convert to string without timezone offset
        # print(current_time.strftime('%Y-%m-%d %H:%M:%S'), "Current Time")
        # print(reminder_time_str, "Reminder Time")
        try:
            if current_time.strftime('%Y-%m-%d %H:%M:%S') == reminder_time_str:
                print("SEND AN EMAIL NOW!")
                # Send the reminder email
                send_reminder_email(task.user.pk, task.pk, reminder_time)
        except Exception as e:
            print(e)
            pass
    
   
 
    
