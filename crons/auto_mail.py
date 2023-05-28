# from apscheduler.schedulers.background import BackgroundScheduler
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from .models import Task

# def send_reminder_email(user_id, task_id, reminder_time):
#     user = User.objects.get(pk=user_id)
#     task = Task.objects.get(pk=task_id)
#     subject = f'Reminder: Task "{task.title}" due soon'
#     message = render_to_string('todo/email_reminder.html', {
#         'user': user,
#         'task': task,
#         'reminder_time': reminder_time
#     })
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user.email]
#     send_mail(subject, message, from_email, recipient_list, fail_silently=False)

# def schedule_reminders():
#     scheduler = BackgroundScheduler()
#     scheduler.start()
#     for task in Task.objects.all():
#         if task.reminder_time > 0:
#             due_date = timezone.localtime(task.due_date)
#             reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)
#             scheduler.add_job(send_reminder_email, 'date', run_date=reminder_time, args=(task.user.pk, task.pk, reminder_time))
            
  
            
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
    # task = Task.objects.get(pk=task_id)

    # # Check if a reminder needs to be sent
    # if task.reminder_time > 0:
    #     due_date = timezone.localtime(task.due_date)
    #     reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)
    #     if timezone.now() >= reminder_time and not task.reminder_sent:
    #         # Send the reminder email
    #         send_reminder_email(task.user.pk, task.pk, reminder_time)
    #         # Mark the task as having a reminder sent
    #         task.reminder_sent = True
    #         task.save()        
    # print("---")
    # print(timezone.now())
    # for task in Task.objects.all():
    #     due_date = timezone.localtime(task.due_date)
    #     reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)
    #     print(timezone.now(), "TZ")
    #     print(reminder_time ,"RT")
    #     try:
    #         if timezone.now() == reminder_time:
    #             # Send the reminder email
    #             send_reminder_email(task.user.pk, task.pk, reminder_time)
    #             # Mark the task as having a reminder sent
    #             # task.reminder_sent = True
    #             # task.save() 
    #     except Exception as e:print(e)
    
    from dateutil.parser import parse
    import pytz
    from django.utils import timezone

    # get the current datetime with timezone information
    now = timezone.localtime()
    print(now, "NOW")

    # iterate through all tasks
    for task in Task.objects.all():
        user_timezone = pytz.timezone('Africa/Kampala')
        due_date = timezone.make_naive(task.due_date, task.user.time_zone)  # create a naive datetime object
        # user_timezone = pytz.timezone('Africa/Kampala')  # set the user timezone to Africa/Kampala
        due_date = user_timezone.localize(due_date)
        reminder_time = due_date - timezone.timedelta(minutes=task.reminder_time)

        # compare the current time and the reminder time (compare only the time portion)
        if now.time() == reminder_time.time():
            # send the reminder email
            send_reminder_email(task.user.pk, task.pk, reminder_time)





"""
from django.core.mail import send_mail

def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email='ronlinapps@gmail.com',  # replace with your email address
        recipient_list=recipient_list,
        fail_silently=False,
    )
    
send_email('Hello', 'This is a test email.', ['ronlinx6@gmail.com'])
"""