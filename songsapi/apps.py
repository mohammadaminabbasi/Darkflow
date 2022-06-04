from django.apps import AppConfig


class SongApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songsapi'

    def ready(self):
        print("start up")
        pass
