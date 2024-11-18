# bot/views.py
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramBotView(View):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

    async def handle_message(self, update: Update):
        """Handle incoming messages"""
        message = update.message
        user_id = message.from_user.id
        text = message.text

        # Process commands or regular messages
        if text.startswith('/'):
            await self.handle_command(message, text.lower())
        else:
            response = await self.process_text(text)
            await self.bot.send_message(
                chat_id=user_id,
                text=response
            )

    async def handle_command(self, message, command):
        """Handle bot commands"""
        chat_id = message.chat.id

        if command == '/start':
            keyboard = [
                [KeyboardButton("Help"), KeyboardButton("Status")],
                [KeyboardButton("Process")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await self.bot.send_message(
                chat_id=chat_id,
                text="Welcome! Send me any text to process.",
                reply_markup=reply_markup
            )
        elif command == '/help':
            await self.bot.send_message(
                chat_id=chat_id,
                text="Send me any text and I'll process it. Use /start to see available commands."
            )

    async def process_text(self, text: str) -> str:
        """Process regular text messages"""
        # Add your text processing logic here
        return f"You said: {text}"

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            update = Update.de_json(data, self.bot)
            asyncio.run(self.handle_message(update))
            return HttpResponse('OK')
        except Exception as e:
            logger.error(f"Error processing update: {str(e)}")
            return HttpResponse(status=500)