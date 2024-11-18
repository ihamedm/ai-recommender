from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telegram import Update, Bot
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
import json
import logging
from asgiref.sync import sync_to_async, async_to_sync

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramBotView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Register handlers
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        self.application.add_handler(
            CommandHandler('start', self.start_command)
        )
        self.application.add_handler(
            CommandHandler('help', self.help_command)
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "Welcome! Send me any text to process."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(
            "Send me any text and I'll process it. Use /start to see available commands."
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        message = update.message
        text = message.text

        # Process the message
        response = await self.process_text(text)
        await message.reply_text(response)

    async def process_text(self, text: str) -> str:
        """Process regular text messages"""
        # Add your text processing logic here
        return f"You said: {text}"

    def post(self, request, token):
        try:
            # Verify token
            if token != settings.TELEGRAM_BOT_TOKEN:
                return HttpResponse(status=403)

            # Parse incoming webhook data
            data = json.loads(request.body)
            update = Update.de_json(data, self.bot)

            # Process update synchronously
            async_to_sync(self.application.process_update)(update)

            return HttpResponse('OK')
        except Exception as e:
            logger.error(f"Error processing update: {str(e)}")
            return HttpResponse(status=500)