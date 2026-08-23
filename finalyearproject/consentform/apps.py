from django.apps import AppConfig


class ConsentformConfig(AppConfig):
    name = 'consentform'

def ready(self):
    import consentform.signals