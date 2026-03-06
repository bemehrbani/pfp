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
        self.updater = None
        self.dispatcher = None
        self.job_queue = None

        # Setup Django integration
        self._setup_django()

        # Initialize handlers
        self._init_handlers()

    def _setup_django(self):
        """Set up Django environment for database access."""
        try:
            # Get project root directory (PFP directory)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Add project root to Python path so backend can be imported
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

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
        if not self.dispatcher:
            logger.warning("Dispatcher not initialized. Handlers will be registered later.")
            return

        try:
            from telegram.ext import CommandHandler

            # Import handlers
            from handlers import (
                # Command handlers
                start_command, help_command,
                campaigns_command, joincampaign_command,
                tasks_command, mytasks_command, claimtask_command,
                profile_command, updateprofile_command,
                leaderboard_command,
                # Callback handlers
                campaign_callback_handler, task_callback_handler, leaderboard_callback_handler,
                # Conversation handlers
                task_proof_conversation, registration_conversation,
                # Message handlers
                handle_text_message, handle_unknown_command,
                # Handler lists
                campaign_handlers, task_handlers, leaderboard_handlers,
                text_message_handler, unknown_command_handler
            )

            # Register command handlers
            self.dispatcher.add_handler(CommandHandler("start", start_command))
            self.dispatcher.add_handler(CommandHandler("help", help_command))
            self.dispatcher.add_handler(CommandHandler("campaigns", campaigns_command))
            self.dispatcher.add_handler(CommandHandler("joincampaign", joincampaign_command))
            self.dispatcher.add_handler(CommandHandler("tasks", tasks_command))
            self.dispatcher.add_handler(CommandHandler("mytasks", mytasks_command))
            self.dispatcher.add_handler(CommandHandler("claimtask", claimtask_command))
            self.dispatcher.add_handler(CommandHandler("profile", profile_command))
            self.dispatcher.add_handler(CommandHandler("updateprofile", updateprofile_command))
            self.dispatcher.add_handler(CommandHandler("leaderboard", leaderboard_command))

            # Register callback query handlers
            for handler in campaign_handlers:
                self.dispatcher.add_handler(handler)
            for handler in task_handlers:
                self.dispatcher.add_handler(handler)
            for handler in leaderboard_handlers:
                self.dispatcher.add_handler(handler)

            # Register conversation handlers
            self.dispatcher.add_handler(task_proof_conversation)
            self.dispatcher.add_handler(registration_conversation)

            # Register message handlers
            self.dispatcher.add_handler(text_message_handler)
            self.dispatcher.add_handler(unknown_command_handler)

            # Add error handler
            self.dispatcher.add_error_handler(self._error_handler)

            logger.info(f"Registered {len(self.dispatcher.handlers)} handlers successfully")

        except ImportError as e:
            logger.error(f"Failed to import handlers: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to register handlers: {e}")
            raise

    def _error_handler(self, update: object, context):
        """Handle errors in bot handlers."""
        logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)

        # Try to send error message to user
        try:
            if update and hasattr(update, 'effective_chat'):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="❌ *An error occurred.*\n\n"
                         "Our team has been notified. Please try again later.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")

    def start_polling(self):
        """Start the bot in polling mode (for development)."""
        from telegram.ext import Updater, CommandHandler

        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        # Initialize handlers
        self._init_handlers()

        logger.info("Starting bot in polling mode...")
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self, webhook_url: str, port: int = 8443):
        """Start the bot in webhook mode (for production)."""
        from telegram.ext import Updater, CommandHandler

        self.updater = Updater(self.token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue

        # Initialize handlers
        self._init_handlers()

        # Set webhook
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=self.token,
            webhook_url=f"{webhook_url}/{self.token}"
        )
        logger.info(f"Webhook set to {webhook_url}/{self.token}")
        self.updater.idle()

    def stop(self):
        """Stop the bot gracefully."""
        if self.updater:
            self.updater.stop()
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