from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-task-reminders': {
        'task': 'todo.email_reminder.send_task_reminders',
        'schedule': crontab(hour='8-17', minute='*/5')
    }
}