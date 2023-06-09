# Generated by Django 4.0 on 2023-05-14 14:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_task_due_date_systemlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='systemlog',
            old_name='message',
            new_name='log_message',
        ),
        migrations.RenameField(
            model_name='systemlog',
            old_name='timestamp',
            new_name='log_time',
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 14, 14, 11, 24, 665774, tzinfo=utc)),
        ),
    ]
