from django.utils import timezone
from todo.models import Task

def auto_delete():
    # Get the relevant objects to delete
    relevant_objects = Task.objects.filter(created__lt=timezone.now() - timezone.timedelta(days=7))

    # Delete the objects
    # print("---")
    relevant_objects.delete()