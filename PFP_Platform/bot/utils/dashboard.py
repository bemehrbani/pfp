"""
Campaign dashboard message composer for Telegram channel.

Builds a branded HTML message showing the campaign definition, OKR progress
bars, available tasks, resource links, and a Join button. Designed to be
sent once, pinned, and then edited in-place every hour with fresh stats.
"""
import logging
from datetime import datetime, timezone as tz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils.brand_constants import (
    BRAND_HEADER_HTML,
    BRAND_FOOTER_HTML,
    BRAND_SEPARATOR,
    BOT_USERNAME,
)

logger = logging.getLogger(__name__)


def render_progress_bar(current: int, target: int, width: int = 10) -> str:
    """
    Render a Unicode progress bar.

    >>> render_progress_bar(45, 100)
    '█████░░░░░  45/100'
    """
    if target <= 0:
        return '░' * width + f'  {current}/—'
    ratio = min(current / target, 1.0)
    filled = round(ratio * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    return f'{bar}  {current}/{target}'


def compose_dashboard_message(
    campaign,
    pulse: dict,
    tasks: list,
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Compose the pinned campaign dashboard HTML message.

    Args:
        campaign: Campaign model instance (with stats fields).
        pulse: Dict from _db_get_campaign_pulse() with total_completed, etc.
        tasks: List of active Task instances for the campaign.

    Returns:
        (html_text, InlineKeyboardMarkup) ready to send or edit.
    """
    now = datetime.now(tz.utc)
    timestamp = now.strftime('%I:%M %p · %b %d, %Y')

    # ── Header ──
    lines = [
        BRAND_HEADER_HTML,
        BRAND_SEPARATOR,
        '',
        f'📢 <b>{_esc(campaign.name)}</b>',
        '',
        f'{_esc(campaign.short_description)}',
        '',
    ]

    # ── OKR Section ──
    lines.append(BRAND_SEPARATOR)
    lines.append('📊 <b>Objectives &amp; Key Results</b>')
    lines.append(BRAND_SEPARATOR)
    lines.append('')

    volunteers_bar = render_progress_bar(
        campaign.current_members, campaign.target_members
    )
    actions_bar = render_progress_bar(
        pulse.get('total_completed', 0), campaign.target_activities
    )
    tweets_bar = render_progress_bar(
        campaign.completed_twitter_posts, campaign.target_twitter_posts
    )

    lines.append(f'🎯 Volunteers:  <code>{volunteers_bar}</code>')
    lines.append(f'📝 Actions:     <code>{actions_bar}</code>')
    lines.append(f'🐦 Tweets:      <code>{tweets_bar}</code>')
    lines.append('')

    progress = campaign.progress_percentage()
    lines.append(f'📈 Overall progress: <b>{progress:.0f}%</b>')
    lines.append('')

    # ── Tasks Section ──
    lines.append(BRAND_SEPARATOR)
    lines.append('🎯 <b>Available Tasks</b>')
    lines.append(BRAND_SEPARATOR)
    lines.append('')

    type_icons = {
        'twitter_post': '🐦', 'twitter_retweet': '🔁',
        'twitter_comment': '💬', 'content_creation': '✍️',
        'petition': '✍️', 'mass_email': '📧',
        'research': '🔍', 'other': '📌',
    }

    for task in tasks:
        icon = type_icons.get(task.task_type, '📌')
        lines.append(
            f'{icon} {_esc(task.title)}  ({task.estimated_time} min)'
        )

    lines.append('')

    # ── Resources Section ──
    lines.append(BRAND_SEPARATOR)
    lines.append('🔗 <b>Resources</b>')
    lines.append(
        '🕯 <a href="https://peopleforpeace.live">Memorial</a>'
        ' · 📄 <a href="https://peopleforpeace.live/evidence.html">Evidence</a>'
        ' · 📊 <a href="https://peopleforpeace.live/data.html">Data</a>'
    )
    lines.append('')

    # ── Footer ──
    lines.append(BRAND_FOOTER_HTML)
    lines.append(f'🔄 Last updated: {timestamp}')

    html_text = '\n'.join(lines)

    # ── Inline Keyboard ──
    deep_link = f'https://t.me/{BOT_USERNAME}?start=campaign_{campaign.id}'
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('➕ Join the Campaign', url=deep_link)],
    ])

    return html_text, keyboard


def _esc(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )
