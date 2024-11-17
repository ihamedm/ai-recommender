from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot


class Command(BaseCommand):
    help = 'Sets up the Telegram webhook'

    def handle(self, *args, **kwargs):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        # Delete existing webhook
        bot.delete_webhook()

        # Set new webhook
        success = bot.set_webhook(settings.WEBHOOK_URL)

        if success:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully set webhook to {settings.WEBHOOK_URL}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('Failed to set webhook')
            )