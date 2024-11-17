from django.urls import path
from .views import TelegramBotView

urlpatterns = [
    path('webhook/<str:token>/', TelegramBotView.as_view(), name='telegram_webhook'),
]