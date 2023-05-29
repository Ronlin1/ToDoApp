from django.db import models
# from django.contrib.auth.models import User
from datetime import date, time, datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

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
    email = models.EmailField(max_length=100, blank=False, null=False, default="ronlinapps@gmail.com")
    
    def save(self, *args, **kwargs):
        if not self.complete and self.due_date <= timezone.now():
            self.skipped = True
        super().save(*args, **kwargs)
        
    # def get_absolute_url(self):
    #     return reverse('tasks-detail', args=[str(self.id)])
    # def get_absolute_url(self, user_id=None):
    #     url = reverse('tasks-detail', args=[str(self.id)])
    #     if user_id:
    #         url += f'?user_id={user_id}'
    #     return url
    def get_absolute_url(self, user_id=None):
        domain_name = settings.DOMAIN_NAME
        url = reverse('tasks-detail', args=[str(self.id)])
        url = f"https://{domain_name}{url}"

        if user_id:
            url += f'?user_id={user_id}'

        return url

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

