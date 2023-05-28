from django.apps import AppConfig

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'
    
    def ready(self):
        from crons import run_crons    
        run_crons.start()
    






