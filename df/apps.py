from django.apps import AppConfig


class DarkflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'darkflow'

    def ready(self):
        # print("start up")
        pass
