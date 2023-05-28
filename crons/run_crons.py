from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .auto_clean import auto_delete
from .auto_mail import auto_send
from .auto_skip import mark_tasks_as_skipped

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_delete, 'interval', days=5, id='auto_delete')
    scheduler.add_job(auto_send, 'interval', seconds=35, id='auto_send')
    scheduler.add_job(mark_tasks_as_skipped, 'interval', seconds=5, id='mark_tasks_as_skipped')
    scheduler.start()
   