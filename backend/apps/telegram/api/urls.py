"""
URLs for Telegram app API.
"""
from django.urls import path
from . import views

app_name = 'telegram'

urlpatterns = [
    # Telegram webhook (no authentication required for Telegram servers)
    path('webhook/<str:bot_token>/', views.TelegramWebhookView.as_view(), name='telegram_webhook'),

    # Bot management (admin only)
    path('status/', views.TelegramBotStatusView.as_view(), name='telegram_status'),
    path('webhook/set/', views.SetTelegramWebhookView.as_view(), name='set_webhook'),
    path('webhook/delete/', views.DeleteTelegramWebhookView.as_view(), name='delete_webhook'),
    path('send-message/', views.SendTelegramMessageView.as_view(), name='send_message'),
]