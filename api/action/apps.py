from django.apps import AppConfig


class ActionConfig(AppConfig):
    name = 'action'

    def ready(self):
        import action.signals
