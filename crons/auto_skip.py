import datetime
from django.utils import timezone
from todo.models import Task

def mark_tasks_as_skipped():
    now = timezone.now()
    Task.objects.filter(complete=False, due_date__lt=now).update(skipped=True)

# import datetime
# from django.conf import settings
# from django.core.mail import send_mail
# from django.utils import timezone
# from todo.models import Task
# from django.contrib.auth.models import User
# def mark_tasks_as_skipped(user_id):
#     user = User.objects.get(pk=user_id)
#     now = timezone.now()
#     incomplete_tasks = Task.objects.filter(complete=False)
#     for task in incomplete_tasks:
#         if task.due_date and now > task.due_date:
#             task.skipped = True
#             task.save()
#             subject = f"Skipped Task Notification: {task.title}"
#             message = f"The following task has been marked as skipped:\n\n"
#             due_date_str = task.due_date.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S %Z')
#             message += f"- {task.title} (due {due_date_str})\n"
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]
#             send_mail(subject, message, from_email, recipient_list)