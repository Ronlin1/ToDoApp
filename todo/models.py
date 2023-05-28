from django.db import models
# from django.contrib.auth.models import User
from datetime import date, time, datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    skipped = models.BooleanField(default=False)
    due_date = models.DateTimeField(default=timezone.now)
    reminder_time = models.IntegerField(null=False, blank=False, default=1)
    email = models.EmailField(max_length=254, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.complete and self.due_date <= timezone.now():
            self.skipped = True
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('tasks-detail', args=[str(self.id)])
    
    # def delete(self, *args, **kwargs):
    #     expired_days_ago = (timezone.now() - self.created).days >= 7
    #     if expired_days_ago:
    #         super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

class SystemLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_time = models.DateTimeField(auto_now_add=True)
    log_message = models.TextField()

    def __str__(self):
        return f'{self.log_time} - {self.log_message}'


# class TaskManager(models.Manager):
#     def delete_old_tasks(self):
#         """
#         Deletes all tasks that are 7 days or older.
#         """
#         self.filter(due_date__lte=timezone.now() - timezone.timedelta(days=7)).delete()


# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     time_zone = models.CharField(max_length=50, default='UTC')