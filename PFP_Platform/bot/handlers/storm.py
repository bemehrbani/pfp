"""
Twitter Storm command handler for Telegram bot.

Provides the /storm command (tweet briefing, tweet serving, hashtag copy,
storm info) and the /send_reminder admin command.

Agent 2 provides:
  - content.twitter_storm_tweets.TWITTER_STORM_TWEETS  (tweet list)
  - utils.translations keys: twitter_storm_*

Issues: #23 (bot integration), #24 (reminders)
"""
import logging
import os
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from asgiref.sync import sync_to_async

from utils.translations import t
from utils.state_management import state_manager

logger = logging.getLogger(__name__)

# Admin IDs from environment (comma-separated)
ADMIN_IDS: list[int] = [
    int(x) for x in os.environ.get('BOT_ADMIN_IDS', '').split(',') if x.strip()
]

CHANNEL_ID = '@people4peace'


# ── Async-safe DB helper ──────────────────────────────────────────────

@sync_to_async
def _get_lang(session) -> str:
    """Get language from session (sync ORM access)."""
    session.refresh_from_db(fields=['language'])
    return session.language or 'en'


# ── /storm command ────────────────────────────────────────────────────

async def storm_command(update: Update, context: CallbackContext):
    """Handle /storm command — show Twitter Storm briefing with action buttons."""
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = await _get_lang(session)

    # Build briefing text from translation key (HTML)
    briefing = t('twitter_storm_briefing', lang)

    keyboard = [
        [InlineKeyboardButton("🐦 Get a Tweet", callback_data="storm_get_tweet")],
        [InlineKeyboardButton("📋 Copy Hashtags", callback_data="storm_hashtags")],
        [InlineKeyboardButton("📆 When & How", callback_data="storm_when_how")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send via bot to handle both /command and callback invocations
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=briefing,
        parse_mode='HTML',
        reply_markup=reply_markup,
    )


# ── Tweet serving ────────────────────────────────────────────────────

def _pick_unseen_tweet(context: CallbackContext, lang: str) -> dict | None:
    """Pick a random unseen tweet for the user, resetting if all seen."""
    try:
        from content.twitter_storm_tweets import TWITTER_STORM_TWEETS
    except ImportError:
        logger.warning("twitter_storm_tweets module not yet available")
        return None

    if not TWITTER_STORM_TWEETS:
        return None

    seen: list = context.user_data.setdefault('seen_storm_tweets', [])
    all_ids = [tw.get('id', idx) for idx, tw in enumerate(TWITTER_STORM_TWEETS)]

    unseen_ids = [tid for tid in all_ids if tid not in seen]
    if not unseen_ids:
        # All seen — reset
        seen.clear()
        unseen_ids = all_ids

    chosen_id = random.choice(unseen_ids)
    seen.append(chosen_id)

    # Find the tweet dict
    for idx, tw in enumerate(TWITTER_STORM_TWEETS):
        if tw.get('id', idx) == chosen_id:
            return tw

    return None


async def _send_tweet(update: Update, context: CallbackContext, lang: str):
    """Send a random unseen tweet in a copyable code block."""
    query = update.callback_query

    tweet = _pick_unseen_tweet(context, lang)
    if tweet is None:
        await query.edit_message_text(
            "⚠️ Tweet library not available yet. Check back soon!",
            parse_mode='HTML',
        )
        return

    # Get text in user's language with fallback to English
    text = tweet.get(f'text_{lang}', tweet.get('text_en', ''))

    message = (
        "🐦 <b>Your Tweet</b>\n\n"
        f"<code>{text}</code>\n\n"
        "👉 Copy the text above,  open Twitter/X, and post it!"
    )

    keyboard = [
        [InlineKeyboardButton("🔄 Get Another", callback_data="storm_get_tweet")],
        [InlineKeyboardButton("📋 Copy Hashtags", callback_data="storm_hashtags")],
        [InlineKeyboardButton("↩️ Back", callback_data="storm_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=message,
        parse_mode='HTML',
        reply_markup=reply_markup,
    )


# ── Hashtags ─────────────────────────────────────────────────────────

async def _send_hashtags(update: Update, context: CallbackContext, lang: str):
    """Show campaign hashtags in a copyable code block."""
    query = update.callback_query

    hashtags = t('twitter_storm_hashtags', lang)

    message = (
        "📋 <b>Copy These Hashtags</b>\n\n"
        f"<code>{hashtags}</code>\n\n"
        "👉 Add these to your tweet for maximum reach!"
    )

    keyboard = [
        [InlineKeyboardButton("🐦 Get a Tweet", callback_data="storm_get_tweet")],
        [InlineKeyboardButton("↩️ Back", callback_data="storm_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=message,
        parse_mode='HTML',
        reply_markup=reply_markup,
    )


# ── When & How (storm info) ──────────────────────────────────────────

async def _send_storm_info(update: Update, context: CallbackContext, lang: str):
    """Show storm date, time, and brief instructions."""
    query = update.callback_query

    message = (
        "📆 <b>Twitter Storm — When & How</b>\n\n"
        "📅 <b>Date:</b> March 28, 2026\n"
        "🕐 <b>Time:</b> 1:00 PM UTC (worldwide)\n"
        "⏱ <b>Duration:</b> 1 hour\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>How to participate:</b>\n"
        "1️⃣ Get a tweet from the bot (tap 🐦 Get a Tweet)\n"
        "2️⃣ Post it on Twitter/X at the scheduled time\n"
        "3️⃣ Use ALL the hashtags for maximum impact\n"
        "4️⃣ Like & retweet other participants' tweets\n\n"
        "💡 <b>Pro tip:</b> Prepare your tweets in advance!\n"
        "Copy several tweets now and schedule them."
    )

    keyboard = [
        [InlineKeyboardButton("🐦 Get a Tweet", callback_data="storm_get_tweet")],
        [InlineKeyboardButton("📋 Copy Hashtags", callback_data="storm_hashtags")],
        [InlineKeyboardButton("↩️ Back", callback_data="storm_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=message,
        parse_mode='HTML',
        reply_markup=reply_markup,
    )


# ── Callback router ──────────────────────────────────────────────────

async def storm_tweet_callback_handler(update: Update, context: CallbackContext):
    """Route storm_* callback queries to the appropriate handler."""
    query = update.callback_query
    await query.answer()

    data = query.data
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = await _get_lang(session)

    if data == 'storm_get_tweet':
        await _send_tweet(update, context, lang)
    elif data == 'storm_hashtags':
        await _send_hashtags(update, context, lang)
    elif data == 'storm_when_how':
        await _send_storm_info(update, context, lang)
    elif data == 'storm_back':
        # Re-show the main briefing
        briefing = t('twitter_storm_briefing', lang)
        keyboard = [
            [InlineKeyboardButton("🐦 Get a Tweet", callback_data="storm_get_tweet")],
            [InlineKeyboardButton("📋 Copy Hashtags", callback_data="storm_hashtags")],
            [InlineKeyboardButton("📆 When & How", callback_data="storm_when_how")],
        ]
        await query.edit_message_text(
            text=briefing,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    else:
        logger.warning(f"Unknown storm callback: {data}")


# ── Issue #24 — Admin Reminder Command ────────────────────────────────

async def admin_send_reminder(update: Update, context: CallbackContext):
    """Admin command: /send_reminder 1w|1d|1h

    Sends a pre-written reminder message to the @people4peace channel.
    Only callable by admin users (BOT_ADMIN_IDS env var).
    """
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return

    if not context.args:
        await update.message.reply_text("Usage: /send_reminder 1w|1d|1h")
        return

    reminder_type = context.args[0]
    key_map = {
        '1w': 'twitter_storm_reminder_1w',
        '1d': 'twitter_storm_reminder_1d',
        '1h': 'twitter_storm_reminder_1h',
    }
    translation_key = key_map.get(reminder_type)
    if not translation_key:
        await update.message.reply_text("Invalid type. Use: 1w, 1d, or 1h")
        return

    message = t(translation_key, 'en')

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode='HTML',
    )
    await update.message.reply_text(
        f"✅ Sent {reminder_type} reminder to {CHANNEL_ID}"
    )


# ── Handler registration ─────────────────────────────────────────────

# NOTE: The existing storms.py uses pattern '^storm_' for its DB-backed
# storm_info_<id> and storm_ready_<id> callbacks. This module's callbacks
# use specific patterns that don't collide: storm_get_tweet, storm_hashtags,
# storm_when_how, storm_back.

storm_tweet_handlers = [
    CommandHandler('storm', storm_command),
    CommandHandler('send_reminder', admin_send_reminder),
    CallbackQueryHandler(
        storm_tweet_callback_handler,
        pattern=r'^storm_(get_tweet|hashtags|when_how|back)$',
    ),
]
