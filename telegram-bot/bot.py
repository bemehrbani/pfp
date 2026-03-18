#!/usr/bin/env python3
"""
Telegram Bot for People for Peace Campaign Manager.
Handles volunteer registration, task claiming, and campaign updates.
"""
import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv

# Add telegram-bot directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class PFPCampaignBot:
    """Main bot class for People for Peace Campaign Manager."""

    def __init__(self, token: Optional[str] = None):
        """Initialize the bot."""
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("Telegram bot token not provided")

        # Initialize bot components
        self.application = None

        # Setup Django integration
        self._setup_django()

    def _setup_django(self):
        """Set up Django environment for database access."""
        try:
            # Get project root directory (PFP directory)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Add project root to Python path so backend can be imported
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            # In Docker, backend is mounted at /app/backend — add it to path
            docker_backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
            if os.path.isdir(docker_backend_path) and docker_backend_path not in sys.path:
                sys.path.insert(0, docker_backend_path)

            # Also add <project_root>/backend for local development
            local_backend_path = os.path.join(project_root, 'backend')
            if os.path.isdir(local_backend_path) and local_backend_path not in sys.path:
                sys.path.insert(0, local_backend_path)

            # Determine settings module based on environment
            settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

            import django
            django.setup()
            logger.info(f"Django setup completed with settings: {settings_module}")

        except Exception as e:
            logger.error(f"Django setup failed: {e}")
            logger.error("Bot cannot run without Django integration")
            raise

    def _init_handlers(self):
        """Initialize bot handlers."""
        if not self.application:
            logger.warning("Application not initialized. Handlers will be registered later.")
            return

        try:
            from telegram.ext import CommandHandler

            # Import handlers
            from handlers import (
                # Command handlers
                start_command, help_command, language_command,
                language_callback_handler,
                campaigns_command, joincampaign_command,
                tasks_command, mytasks_command, claimtask_command,
                profile_command, updateprofile_command,
                storms_command, storminfo_command,
                # Callback handlers
                campaign_callback_handler, task_callback_handler,
                storm_callback_handler,
                # Menu callback handler
                menu_callback_handler,
                # Conversation handlers
                task_proof_conversation, registration_conversation,
                # Message handlers
                handle_text_message, handle_unknown_command,
                # Handler lists
                campaign_handlers, task_handlers,
                storm_handlers, menu_handlers,
                # Storm tweet handlers (storm.py — /storm command)
                storm_tweet_handlers,
                text_message_handler, unknown_command_handler
            )

            # Import dashboard auth handler
            from handlers.dashboard_auth import dashboard_command
            from handlers.dashboard_channel import (
                post_dashboard_command, refresh_dashboard_command,
            )

            # Register command handlers
            self.application.add_handler(CommandHandler("start", start_command))
            self.application.add_handler(CommandHandler("help", help_command))
            self.application.add_handler(CommandHandler("campaigns", campaigns_command))
            self.application.add_handler(CommandHandler("joincampaign", joincampaign_command))
            self.application.add_handler(CommandHandler("tasks", tasks_command))
            self.application.add_handler(CommandHandler("mytasks", mytasks_command))
            self.application.add_handler(CommandHandler("claimtask", claimtask_command))
            self.application.add_handler(CommandHandler("profile", profile_command))
            self.application.add_handler(CommandHandler("updateprofile", updateprofile_command))

            self.application.add_handler(CommandHandler("storms", storms_command))
            self.application.add_handler(CommandHandler("storminfo", storminfo_command))
            self.application.add_handler(CommandHandler("language", language_command))
            self.application.add_handler(CommandHandler("dashboard", dashboard_command))
            self.application.add_handler(CommandHandler("post_dashboard", post_dashboard_command))
            self.application.add_handler(CommandHandler("refresh_dashboard", refresh_dashboard_command))

            # Register language callback handler (before other callback handlers)
            from telegram.ext import CallbackQueryHandler
            self.application.add_handler(
                CallbackQueryHandler(language_callback_handler, pattern=r"^lang_")
            )

            # Register callback query handlers
            for handler in campaign_handlers:
                self.application.add_handler(handler)
            for handler in task_handlers:
                self.application.add_handler(handler)

            for handler in storm_handlers:
                self.application.add_handler(handler)
            for handler in storm_tweet_handlers:
                self.application.add_handler(handler)
            for handler in menu_handlers:
                self.application.add_handler(handler)

            # Register conversation handler (registration only;
            # task_proof_conversation is already in task_handlers)
            self.application.add_handler(registration_conversation)

            # Register message handlers
            self.application.add_handler(text_message_handler)
            self.application.add_handler(unknown_command_handler)

            # Add error handler
            self.application.add_error_handler(self._error_handler)

            logger.info("Handlers registered successfully")

        except ImportError as e:
            logger.error(f"Failed to import handlers: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to register handlers: {e}")
            raise

    async def _error_handler(self, update: object, context):
        """Handle errors in bot handlers."""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)

        # Try to send error message to user
        try:
            if update and hasattr(update, 'effective_chat'):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ *An error occurred.*\n\n"
                         "Our team has been notified. Please try again later.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

    def start_polling(self):
        """Start the bot in polling mode (for development)."""
        from telegram.ext import Application

        self.application = Application.builder().token(self.token).build()

        # Initialize handlers
        self._init_handlers()

        logger.info("Starting bot in polling mode...")
        self.application.run_polling(
            allowed_updates=[
                'message', 'callback_query', 'edited_message',
                'channel_post', 'my_chat_member', 'chat_member'
            ]
        )

    def start_webhook(self, webhook_url: str, port: int = 8443):
        """Start the bot in webhook mode (for production)."""
        from telegram.ext import Application

        self.application = Application.builder().token(self.token).build()

        # Initialize handlers
        self._init_handlers()

        logger.info(f"Starting bot in webhook mode on port {port}...")
        self.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=self.token,
            webhook_url=f"{webhook_url}/{self.token}"
        )

    def stop(self):
        """Stop the bot gracefully."""
        if self.application:
            logger.info("Bot stopped")


def main():
    """Main entry point for the bot."""
    import argparse

    parser = argparse.ArgumentParser(description='People for Peace Campaign Bot')
    parser.add_argument('--mode', choices=['polling', 'webhook'], default='polling',
                       help='Bot mode (default: polling)')
    parser.add_argument('--webhook-url', help='Webhook URL for production mode')
    parser.add_argument('--port', type=int, default=8443, help='Port for webhook server')

    args = parser.parse_args()

    try:
        bot = PFPCampaignBot()

        if args.mode == 'webhook':
            if not args.webhook_url:
                logger.error("Webhook URL required for webhook mode")
                return
            bot.start_webhook(args.webhook_url, args.port)
        else:
            bot.start_polling()

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == '__main__':
    main()