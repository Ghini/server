from django.core.management.base import BaseCommand

# custom management command to create the guest user.

# it's just guest/guest, with no special privileges
#


class Command(BaseCommand):
    help = 'create the guest/guest user'

    def handle(self, *args, **kwargs):
        from django.contrib.auth.models import User
        guest, _ = User.objects.get_or_create(username='guest')
        guest.set_password('guest')
        guest.save()
