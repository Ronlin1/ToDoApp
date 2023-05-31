from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Task
from django.core.management import call_command
# from todo.management.commands.delete_old_tasks import Command

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='top_secret')
        self.task = Task.objects.create(
            user=self.user,
            title='Test task',
            description='This is a test task',
            complete=False,
            skipped=False,
            due_date=timezone.now() + timezone.timedelta(days=1),
        )

    def test_task_is_not_skipped_if_not_complete_and_not_past_due_date(self):
        self.task.complete = False
        self.task.due_date = timezone.now() + timezone.timedelta(days=1)
        self.task.save()
        self.assertFalse(self.task.skipped)

    def test_task_is_skipped_if_not_complete_and_past_due_date(self):
        self.task.complete = False
        self.task.due_date = timezone.now() - timezone.timedelta(days=1)
        self.task.save()
        self.assertTrue(self.task.skipped)

    def test_task_is_not_skipped_if_complete_and_past_due_date(self):
        self.task.complete = True
        self.task.due_date = timezone.now() - timezone.timedelta(days=1)
        self.task.save()
        self.assertFalse(self.task.skipped)
        

