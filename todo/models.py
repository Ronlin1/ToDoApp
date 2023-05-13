from django.db import models
# from django.contrib.auth.models import User
from datetime import date, time
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    skipped = models.BooleanField(default=False)
    due_date = models.DateField(default= date.today)
    reminder_time = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.complete and self.due_date <= timezone.now().date():
            self.skipped = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
      

