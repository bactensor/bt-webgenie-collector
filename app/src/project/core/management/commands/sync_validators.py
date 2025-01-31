from django.core.management.base import BaseCommand

from ...tasks import sync_validators


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_validators()
