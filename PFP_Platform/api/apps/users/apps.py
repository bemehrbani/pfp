from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = _('Users')

    def ready(self):
        # Import signals
        try:
            import apps.users.signals  # noqa
            from django.contrib.auth.signals import user_logged_in, user_logged_out
            from apps.users.signals import user_logged_in as user_logged_in_handler
            from apps.users.signals import user_logged_out as user_logged_out_handler

            # Connect signals
            user_logged_in.connect(user_logged_in_handler)
            user_logged_out.connect(user_logged_out_handler)
        except ImportError:
            pass