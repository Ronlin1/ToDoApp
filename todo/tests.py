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
        

class TaskDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='top_secret')

        # Create a task that is 6 days old
        self.old_task = Task.objects.create(
            user=self.user,
            title='Test task (old)',
            description='This is a test task due 6 days ago and complete',
            complete=True,
            skipped=False,
            due_date=timezone.now() - timezone.timedelta(days=6),
        )

        # Create a task that is 8 days old
        self.older_task = Task.objects.create(
            user=self.user,
            title='Test task (older)',
            description='This is a test task due 8 days ago and complete',
            complete=True,
            skipped=False,
            due_date=timezone.now() - timezone.timedelta(days=8),
        )

    def test_delete_old_tasks_deletes_old_tasks(self):
        # Verify that the old task exists before calling delete_old_tasks()
        self.assertTrue(Task.objects.filter(id=self.old_task.id).exists())

        # Verify that the older task exists before calling delete_old_tasks()
        self.assertTrue(Task.objects.filter(id=self.older_task.id).exists())

        # Call delete_old_tasks() and verify that the older task has been deleted
        call_command('delete_old_tasks')
        self.assertFalse(Task.objects.filter(id=self.old_task.id).exists())
        self.assertFalse(Task.objects.filter(id=self.older_task.id).exists())