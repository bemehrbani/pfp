"""
Admin bot commands for tweet target management.

Commands:
    /discover_tweets — Discover tweets, preview, and approve before committing
    /tweet_targets   — List currently active KeyTweet records
    /find_tweets     — Manually paste URLs to force-add specific tweets
    /clear_tweets    — Deactivate all active tweet targets

Approval flow:
    /discover_tweets → bot fetches & scores tweets → shows preview →
    admin taps ✅ Approve All or ❌ Cancel → only then KeyTweets are created
"""
import logging
import os
import re
from typing import List, Tuple

import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
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
# /discover_tweets — Preview + Approval flow
# ─────────────────────────────────────────────────────────────────

async def cmd_discover_tweets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: discover tweets and show preview for approval."""
    if not _is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "🔍 Searching for relevant tweets... This may take 30–60 seconds.",
    )

    from services.tweet_discovery import preview_tweets

    result = await preview_tweets(count=20)

    if result['status'] in ('error', 'disabled'):
        await update.message.reply_text(f"❌ {result['message']}")
        return

    if result['status'] == 'warning':
        await update.message.reply_text(f"⚠️ {result['message']}")
        return

    tweets = result.get('tweets', [])
    if not tweets:
        await update.message.reply_text("No tweets found.")
        return

    # Store candidates in bot_data for the approval callback
    approval_key = f"tweet_preview_{update.effective_user.id}"
    context.bot_data[approval_key] = {
        'tweets': tweets,
        'source': result.get('source', 'unknown'),
    }

    # Build preview message
    preview = (
        f"📋 <b>Tweet Discovery Preview</b>\n"
        f"📡 Source: {result.get('source', 'unknown')}\n"
        f"🔢 Found: {len(tweets)} candidates\n\n"
    )

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    # Show top 10 in preview
    for idx, tweet in enumerate(tweets[:10]):
        emoji = emojis[idx] if idx < 10 else f"{idx + 1}."
        text_snippet = tweet.get('text', '')[:70]
        score = tweet.get('score', 0)
        ellipsis = '...' if len(tweet.get('text', '')) > 70 else ''
        preview += (
            f"{emoji} <b>{tweet.get('author_handle', '')}</b> "
            f"<i>(score: {score:.0f})</i>\n"
            f"   {text_snippet}{ellipsis}\n"
            f"   🔗 {tweet['url']}\n\n"
        )

    if len(tweets) > 10:
        preview += f"<i>...and {len(tweets) - 10} more tweets.</i>\n\n"

    preview += "<b>Approve these as today's engagement targets?</b>"

    # Approval buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"✅ Approve All ({len(tweets)})",
                callback_data="tweet_target_approve_all",
            ),
            InlineKeyboardButton(
                "✅ Approve Top 10",
                callback_data="tweet_target_approve_top10",
            ),
        ],
        [
            InlineKeyboardButton(
                "✅ Approve Top 5",
                callback_data="tweet_target_approve_top5",
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="tweet_target_cancel",
            ),
        ],
    ])

    await update.message.reply_text(
        preview,
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


async def _handle_approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle approval/cancel button press from tweet preview."""
    query = update.callback_query
    await query.answer()

    if not _is_admin(query.from_user.id):
        return

    action = query.data  # tweet_target_approve_all / _top10 / _top5 / _cancel

    # ── Cancel ──
    if action == 'tweet_target_cancel':
        approval_key = f"tweet_preview_{query.from_user.id}"
        context.bot_data.pop(approval_key, None)
        await query.edit_message_text("❌ Discovery cancelled. No changes made.")
        return

    # ── Approve ──
    approval_key = f"tweet_preview_{query.from_user.id}"
    preview_data = context.bot_data.pop(approval_key, None)

    if not preview_data:
        await query.edit_message_text(
            "⚠️ Preview expired. Run /discover_tweets again."
        )
        return

    tweets = preview_data['tweets']
    source = preview_data['source']

    # Determine how many to approve
    if action == 'tweet_target_approve_top5':
        tweets = tweets[:5]
    elif action == 'tweet_target_approve_top10':
        tweets = tweets[:10]
    # else approve_all: keep full list

    await query.edit_message_text("⏳ Committing approved tweets...")

    from services.tweet_discovery import commit_tweets, format_channel_message

    result = await commit_tweets(tweets)

    if result.get('status') == 'error':
        await query.edit_message_text(f"❌ {result['message']}")
        return

    # Post to channel
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
        f"✅ <b>Approved & Committed</b>\n\n"
        f"📡 Source: {source}\n"
        f"🗑️ Deactivated: {result.get('deactivated', 0)} old targets\n"
        f"✨ Created: {result.get('created', 0)} new targets\n"
        f"📢 Posted to channel\n\n"
    )
    for idx, tweet in enumerate(tweets[:5]):
        text_snippet = tweet.get('text', '')[:60]
        report += f"{idx + 1}. {tweet.get('author_handle', '')} — {text_snippet}...\n"

    if len(tweets) > 5:
        report += f"\n...and {len(tweets) - 5} more."

    await query.edit_message_text(report, parse_mode='HTML')


# ─────────────────────────────────────────────────────────────────
# Scheduled discovery → sends preview to admin DM
# ─────────────────────────────────────────────────────────────────

async def send_scheduled_preview(context: ContextTypes.DEFAULT_TYPE):
    """
    Called by the 6h scheduler. Sends a preview to all admins
    instead of auto-committing.
    """
    from services.tweet_discovery import preview_tweets

    result = await preview_tweets(count=20)

    if result.get('status') != 'success' or not result.get('tweets'):
        logger.warning(
            f"Scheduled preview: {result.get('status')} — "
            f"{result.get('message', 'no tweets')}"
        )
        return

    tweets = result['tweets']
    source = result.get('source', 'unknown')

    # Build preview message
    preview = (
        f"🔔 <b>Scheduled Tweet Discovery</b>\n"
        f"📡 Source: {source}\n"
        f"🔢 Found: {len(tweets)} candidates\n\n"
    )

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    for idx, tweet in enumerate(tweets[:5]):
        emoji = emojis[idx] if idx < 5 else f"{idx + 1}."
        text_snippet = tweet.get('text', '')[:70]
        ellipsis = '...' if len(tweet.get('text', '')) > 70 else ''
        preview += (
            f"{emoji} <b>{tweet.get('author_handle', '')}</b>\n"
            f"   {text_snippet}{ellipsis}\n"
            f"   🔗 {tweet['url']}\n\n"
        )

    if len(tweets) > 5:
        preview += f"<i>...and {len(tweets) - 5} more.</i>\n\n"

    preview += "<b>Approve these as today's targets?</b>"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"✅ Approve All ({len(tweets)})",
                callback_data="tweet_target_approve_all",
            ),
            InlineKeyboardButton(
                "✅ Top 10",
                callback_data="tweet_target_approve_top10",
            ),
        ],
        [
            InlineKeyboardButton(
                "✅ Top 5",
                callback_data="tweet_target_approve_top5",
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="tweet_target_cancel",
            ),
        ],
    ])

    # Send to each admin's DM
    for admin_id in BOT_ADMIN_IDS:
        # Store preview data for this admin
        approval_key = f"tweet_preview_{admin_id}"
        context.bot_data[approval_key] = {
            'tweets': tweets,
            'source': source,
        }

        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=preview,
                parse_mode='HTML',
                disable_web_page_preview=True,
                reply_markup=keyboard,
            )
        except Exception as exc:
            logger.error(f"Failed to send scheduled preview to admin {admin_id}: {exc}")


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
# /add_account — Add a monitored Twitter account
# ─────────────────────────────────────────────────────────────────

async def cmd_add_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: add a Twitter account to the monitored list."""
    if not _is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /add_account @handle\n"
            "Example: /add_account @amnesty",
        )
        return

    handle = context.args[0].lstrip('@')
    if not re.match(r'^[A-Za-z0-9_]{1,15}$', handle):
        await update.message.reply_text(f"❌ Invalid handle: @{handle}")
        return

    from services.nitter_client import add_monitored_account

    if add_monitored_account(handle):
        await update.message.reply_text(
            f"✅ @{handle} added to monitored accounts.\n"
            f"Their relevant tweets will appear in /discover_tweets results.",
        )
    else:
        await update.message.reply_text(f"⏭️ @{handle} is already monitored.")


async def cmd_remove_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: remove a Twitter account from the monitored list."""
    if not _is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /remove_account @handle",
        )
        return

    handle = context.args[0].lstrip('@')

    from services.nitter_client import remove_monitored_account

    if remove_monitored_account(handle):
        await update.message.reply_text(f"✅ @{handle} removed from monitored accounts.")
    else:
        await update.message.reply_text(f"❌ @{handle} is not in your custom account list.")


async def cmd_list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: list all monitored Twitter accounts."""
    if not _is_admin(update.effective_user.id):
        return

    from services.nitter_client import get_monitored_accounts

    info = get_monitored_accounts()
    defaults = info['default']
    custom = info['custom']

    msg = "<b>📡 Monitored Accounts</b>\n\n"
    msg += f"<b>Default ({len(defaults)}):</b>\n"
    for handle in defaults:
        msg += f"  • @{handle}\n"

    if custom:
        msg += f"\n<b>Custom ({len(custom)}):</b>\n"
        for handle in custom:
            msg += f"  • @{handle}\n"
    else:
        msg += "\n<i>No custom accounts. Use /add_account @handle to add.</i>\n"

    msg += f"\n<b>Total: {len(info['all'])} accounts</b>"
    await update.message.reply_text(msg, parse_mode='HTML')


# ─────────────────────────────────────────────────────────────────
# /add_tweet — Inline key tweet addition (single step)
# ─────────────────────────────────────────────────────────────────

async def cmd_add_tweet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: add a specific tweet as a key tweet target inline."""
    if not _is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /add_tweet <tweet_url>\n"
            "Example: /add_tweet https://x.com/amnesty/status/123456789",
        )
        return

    text = ' '.join(context.args)
    url_match = TWEET_URL_PATTERN.search(text)

    if not url_match:
        await update.message.reply_text(
            "❌ No valid tweet URL found.\n"
            "Send an x.com or twitter.com link.",
        )
        return

    handle = url_match.group(1)
    tweet_id = url_match.group(2)
    tweet_url = f"https://x.com/{handle}/status/{tweet_id}"

    from apps.tasks.models import Task, KeyTweet

    task = await sync_to_async(
        lambda: Task.objects.filter(
            task_type='twitter_comment', is_active=True,
        ).first()
    )()

    if not task:
        await update.message.reply_text("❌ No active twitter_comment task found.")
        return

    # Check duplicate
    exists = await sync_to_async(
        lambda: KeyTweet.objects.filter(
            tweet_url=tweet_url, task=task, is_active=True,
        ).exists()
    )()

    if exists:
        await update.message.reply_text(f"⏭️ This tweet is already an active target.")
        return

    # Fetch metadata via oEmbed
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
        pass

    # Get max order
    max_order = await sync_to_async(
        lambda: KeyTweet.objects.filter(task=task, is_active=True).count()
    )()

    await sync_to_async(KeyTweet.objects.create)(
        task=task,
        tweet_url=tweet_url,
        author_name=author_name[:200],
        author_handle=f"@{handle}",
        description=description,
        order=max_order,
        is_active=True,
    )

    snippet = f"\n{description[:80]}..." if description else ''
    await update.message.reply_text(
        f"✅ <b>Added tweet target</b>\n\n"
        f"👤 @{handle}{snippet}\n"
        f"🔗 {tweet_url}",
        parse_mode='HTML',
        disable_web_page_preview=True,
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
add_account_handler = CommandHandler('add_account', cmd_add_account)
remove_account_handler = CommandHandler('remove_account', cmd_remove_account)
list_accounts_handler = CommandHandler('list_accounts', cmd_list_accounts)
add_tweet_handler = CommandHandler('add_tweet', cmd_add_tweet)

# Callback handler for approval buttons
approval_callback_handler = CallbackQueryHandler(
    _handle_approval_callback,
    pattern=r'^tweet_target_(approve_all|approve_top10|approve_top5|cancel)$',
)

# Convenience list for registration in bot.py
tweet_target_handlers = [
    find_tweets_conversation,
    discover_tweets_handler,
    tweet_targets_handler,
    clear_tweets_handler,
    add_account_handler,
    remove_account_handler,
    list_accounts_handler,
    add_tweet_handler,
    approval_callback_handler,
]
