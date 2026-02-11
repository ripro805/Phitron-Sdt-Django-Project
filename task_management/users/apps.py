from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field='dgango.db.models.BigAutoField'
    name = "users"
    def ready(self):
        import users.signals
    
