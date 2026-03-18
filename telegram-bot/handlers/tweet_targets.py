"""
Admin bot commands for tweet target management.

Commands:
    /discover_tweets — Trigger automated discovery pipeline
    /tweet_targets   — List currently active KeyTweet records
    /find_tweets     — Manually paste URLs to force-add specific tweets
    /clear_tweets    — Deactivate all active tweet targets
"""
import logging
import os
import re
from typing import List, Tuple

import aiohttp
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

BOT_ADMIN_IDS = [
    int(x) for x in os.getenv('BOT_ADMIN_IDS', '').split(',') if x.strip()
]
TWEET_URL_PATTERN = re.compile(
    r'https?://(?:twitter\.com|x\.com)/(\w+)/status/(\d+)'
)

AWAITING_TWEET_URLS = 0


def _is_admin(user_id: int) -> bool:
    """Check if a Telegram user is a bot admin."""
    return user_id in BOT_ADMIN_IDS


# ─────────────────────────────────────────────────────────────────
# /discover_tweets — Trigger auto-discovery
# ─────────────────────────────────────────────────────────────────

async def cmd_discover_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: manually trigger the automated discovery pipeline."""
    if not _is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "🔍 Starting tweet discovery... This may take 30–60 seconds.",
    )

    from services.tweet_discovery import discover_top_tweets, format_channel_message

    result = await discover_top_tweets(count=20)

    if result['status'] in ('error', 'disabled'):
        await update.message.reply_text(f"❌ {result['message']}")
        return

    if result['status'] == 'warning':
        await update.message.reply_text(f"⚠️ {result['message']}")
        return

    # Post to channel
    tweets = result.get('tweets', [])
    if tweets:
        channel_id = os.getenv('TWEET_CHANNEL_ID', '@people4peace')
        channel_msg = format_channel_message(tweets)
        try:
            await context.bot.send_message(
                chat_id=channel_id,
                text=channel_msg,
                parse_mode='HTML',
                disable_web_page_preview=True,
            )
        except Exception as exc:
            logger.error(f"Channel post failed: {exc}")

    # Report to admin
    report = (
        f"✅ <b>Discovery Complete</b>\n\n"
        f"📡 Source: {result['source']}\n"
        f"🗑️ Deactivated: {result['deactivated']} old targets\n"
        f"✨ Created: {result['created']} new targets\n\n"
    )
    for idx, tweet in enumerate(tweets[:5]):
        text_snippet = tweet.get('text', '')[:60]
        report += f"{idx + 1}. {tweet.get('author_handle', '')} — {text_snippet}...\n"

    if len(tweets) > 5:
        report += f"\n...and {len(tweets) - 5} more."

    await update.message.reply_text(report, parse_mode='HTML')


# ─────────────────────────────────────────────────────────────────
# /tweet_targets — List active targets
# ─────────────────────────────────────────────────────────────────

async def cmd_tweet_targets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: list active KeyTweet records."""
    if not _is_admin(update.effective_user.id):
        return

    from apps.tasks.models import Task, KeyTweet

    task = await sync_to_async(
        lambda: Task.objects.filter(
            task_type='twitter_comment', is_active=True
        ).first()
    )()

    if not task:
        await update.message.reply_text("❌ No active twitter_comment task found.")
        return

    key_tweets = await sync_to_async(
        lambda: list(
            KeyTweet.objects.filter(task=task, is_active=True).order_by('order')
        )
    )()

    if not key_tweets:
        await update.message.reply_text(
            "📋 No active tweet targets.\n"
            "Run /discover_tweets to find new ones."
        )
        return

    msg = f"📋 <b>Active Tweet Targets ({len(key_tweets)})</b>\n\n"
    for idx, kt in enumerate(key_tweets):
        desc = kt.description[:60] + '...' if len(kt.description) > 60 else kt.description
        msg += (
            f"{idx + 1}. <b>{kt.author_handle}</b> — <i>{desc}</i>\n"
            f"   🔗 {kt.tweet_url}\n\n"
        )

    from django.utils.timesince import timesince
    oldest = key_tweets[-1]
    msg += f"<i>Last updated: {timesince(oldest.created_at)} ago</i>"

    await update.message.reply_text(
        msg, parse_mode='HTML', disable_web_page_preview=True,
    )


# ─────────────────────────────────────────────────────────────────
# /find_tweets — Manual URL paste (override)
# ─────────────────────────────────────────────────────────────────

async def cmd_find_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: start manual URL entry flow."""
    if not _is_admin(update.effective_user.id):
        return ConversationHandler.END

    await update.message.reply_text(
        "📎 <b>Manual Tweet Entry</b>\n\n"
        "Paste tweet URLs (one per line). I'll extract the author info "
        "and add them as extra targets alongside the auto-discovered ones.\n\n"
        "Send /cancel to abort.",
        parse_mode='HTML',
    )
    return AWAITING_TWEET_URLS


async def _process_tweet_urls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process pasted tweet URLs and create KeyTweet records."""
    text = update.message.text
    url_matches: List[Tuple[str, str]] = TWEET_URL_PATTERN.findall(text)

    if not url_matches:
        await update.message.reply_text(
            "❌ No valid tweet URLs found. Send x.com or twitter.com links.",
        )
        return AWAITING_TWEET_URLS

    from apps.tasks.models import Task, KeyTweet

    task = await sync_to_async(
        lambda: Task.objects.filter(
            task_type='twitter_comment', is_active=True
        ).first()
    )()

    if not task:
        await update.message.reply_text("❌ No active twitter_comment task found.")
        return ConversationHandler.END

    # Get current max order so we append after existing targets
    max_order = await sync_to_async(
        lambda: KeyTweet.objects.filter(task=task, is_active=True).count()
    )()

    created = 0
    report = "✅ <b>Added Tweet Targets:</b>\n\n"

    for idx, (handle, tweet_id) in enumerate(url_matches):
        tweet_url = f"https://x.com/{handle}/status/{tweet_id}"

        # Check for duplicates
        exists = await sync_to_async(
            lambda url=tweet_url: KeyTweet.objects.filter(
                tweet_url=url, task=task, is_active=True,
            ).exists()
        )()
        if exists:
            report += f"⏭️ @{handle} — already active, skipped\n"
            continue

        # Fetch metadata via Twitter oEmbed (free, no auth)
        author_name = handle
        description = ''
        try:
            oembed_url = (
                f"https://publish.twitter.com/oembed"
                f"?url={tweet_url}&omit_script=true"
            )
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    oembed_url,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        author_name = data.get('author_name', handle)
                        html = data.get('html', '')
                        description = re.sub(r'<[^>]+>', '', html).strip()[:200]
        except Exception:
            pass  # Fallback to handle-only

        await sync_to_async(KeyTweet.objects.create)(
            task=task,
            tweet_url=tweet_url,
            author_name=author_name[:200],
            author_handle=f"@{handle}",
            description=description,
            order=max_order + idx,
            is_active=True,
        )
        created += 1
        snippet = f" — {description[:50]}..." if description else ''
        report += f"✅ @{handle}{snippet}\n"

    report += f"\n<b>Added {created} new target(s).</b>"
    await update.message.reply_text(report, parse_mode='HTML')
    return ConversationHandler.END


async def _cancel_find_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel manual URL entry."""
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


# ─────────────────────────────────────────────────────────────────
# /clear_tweets — Deactivate all targets
# ─────────────────────────────────────────────────────────────────

async def cmd_clear_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: deactivate all active tweet targets."""
    if not _is_admin(update.effective_user.id):
        return

    from apps.tasks.models import Task, KeyTweet

    task = await sync_to_async(
        lambda: Task.objects.filter(
            task_type='twitter_comment', is_active=True
        ).first()
    )()

    if not task:
        await update.message.reply_text("❌ No active twitter_comment task found.")
        return

    count = await sync_to_async(
        lambda: KeyTweet.objects.filter(task=task, is_active=True).update(is_active=False)
    )()

    await update.message.reply_text(
        f"🗑️ Deactivated {count} tweet target(s).\n"
        f"Run /discover_tweets to find new ones.",
    )


# ─────────────────────────────────────────────────────────────────
# Handler registration objects
# ─────────────────────────────────────────────────────────────────

find_tweets_conversation = ConversationHandler(
    entry_points=[CommandHandler('find_tweets', cmd_find_tweets)],
    states={
        AWAITING_TWEET_URLS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                _process_tweet_urls,
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', _cancel_find_tweets)],
)

discover_tweets_handler = CommandHandler('discover_tweets', cmd_discover_tweets)
tweet_targets_handler = CommandHandler('tweet_targets', cmd_tweet_targets)
clear_tweets_handler = CommandHandler('clear_tweets', cmd_clear_tweets)

# Convenience list for registration in bot.py
tweet_target_handlers = [
    find_tweets_conversation,
    discover_tweets_handler,
    tweet_targets_handler,
    clear_tweets_handler,
]
