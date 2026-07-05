"""
Tweet Discovery Engine.

Core logic for finding, scoring, deduplicating, and rotating tweet targets.
Called automatically every 6 hours via JobQueue, or manually via /discover_tweets.
"""
import logging
import os
import re
from datetime import timedelta
from typing import Dict, List, Optional

from asgiref.sync import sync_to_async
from django.utils import timezone

from .nitter_client import fetch_all_tweets, PRIORITY_ACCOUNTS
from .apify_client import fetch_all_tweets_apify

logger = logging.getLogger(__name__)


def _score_tweet(tweet: Dict) -> float:
    """
    Score a tweet for engagement potential.

    Tweets with higher scores are better targets for volunteer engagement.
    The scoring considers engagement metrics, author authority, keyword
    relevance, and whether the account is on our priority list.
    """
    score = 0.0

    # ── Engagement signals (available from Apify, zero from RSS) ──
    score += tweet.get('retweet_count', 0) * 0.5
    score += tweet.get('reply_count', 0) * 0.3
    score += tweet.get('like_count', 0) * 0.1
    score += tweet.get('quote_count', 0) * 0.4

    # ── Follower-count boost ──
    followers = tweet.get('follower_count', 0)
    if followers > 100_000:
        score += 50
    elif followers > 10_000:
        score += 30
    elif followers > 1_000:
        score += 15

    # ── Priority account bonus ──
    handle = tweet.get('author_handle', '').lstrip('@')
    if handle in PRIORITY_ACCOUNTS:
        score += 40

    # ── Keyword relevance bonus ──
    text = tweet.get('text', '').lower()
    high_value_keywords = [
        '168 children', 'minab school', 'war crime', 'airstrike',
        'children killed', 'school attack', 'justice',
    ]
    for keyword in high_value_keywords:
        if keyword in text:
            score += 10

    # ── Base score for RSS-discovered tweets (no engagement data) ──
    has_engagement = any(
        tweet.get(key) for key in ('retweet_count', 'like_count', 'reply_count')
    )
    if not has_engagement:
        score += 20

    return score


def _normalize_tweet_url(url: str) -> str:
    """Normalize tweet URL to canonical x.com format."""
    match = re.search(r'(?:twitter\.com|x\.com)/(\w+)/status/(\d+)', url)
    if match:
        return f"https://x.com/{match.group(1)}/status/{match.group(2)}"
    return ''


async def preview_tweets(count: int = 20) -> Dict:
    """
    Fetch, score, and rank tweets WITHOUT writing to the database.

    This is the first stage of the approval flow. Returns candidates
    for the admin to review before committing.

    Returns:
        Dict with status, source, and ranked tweet candidates
    """
    # Check kill switch
    if os.getenv('TWEET_DISCOVERY_ENABLED', 'true').lower() != 'true':
        logger.info("Tweet discovery disabled via TWEET_DISCOVERY_ENABLED")
        return {'status': 'disabled', 'message': 'Discovery disabled'}

    from apps.tasks.models import Task, KeyTweet

    # ── 1. Find the active twitter_comment task ──
    task = await sync_to_async(
        lambda: Task.objects.filter(task_type='twitter_comment', is_active=True).first()
    )()

    if not task:
        logger.error("No active twitter_comment task found")
        return {'status': 'error', 'message': 'No active twitter_comment task'}

    # ── 2. Fetch tweets from Nitter (primary) ──
    logger.info("Starting tweet discovery via Nitter RSS...")
    raw_tweets = await fetch_all_tweets()
    source = 'nitter'

    # ── 3. Fallback to Apify if Nitter is empty ──
    if not raw_tweets:
        logger.warning("Nitter returned 0 results — trying Apify fallback...")
        raw_tweets = await fetch_all_tweets_apify()
        source = 'apify'

    if not raw_tweets:
        logger.error("Both Nitter and Apify returned 0 results")
        return {'status': 'error', 'message': 'No tweets found from any source'}

    # ── 4. Deduplicate by URL ──
    seen_urls: set = set()
    unique_tweets: List[Dict] = []
    for tweet in raw_tweets:
        normalized = _normalize_tweet_url(tweet['url'])
        if normalized and normalized not in seen_urls:
            seen_urls.add(normalized)
            tweet['url'] = normalized
            unique_tweets.append(tweet)

    # ── 5. Filter out tweets used in the last 7 days ──
    recent_urls = await sync_to_async(
        lambda: set(
            KeyTweet.objects.filter(
                task=task,
                created_at__gte=timezone.now() - timedelta(days=7),
            ).values_list('tweet_url', flat=True)
        )
    )()

    candidates = [t for t in unique_tweets if t['url'] not in recent_urls]

    # ── 6. Score and rank ──
    for tweet in candidates:
        tweet['score'] = _score_tweet(tweet)

    ranked = sorted(candidates, key=lambda t: t['score'], reverse=True)
    top = ranked[:count]

    if not top:
        logger.warning("No new eligible tweets after filtering")
        return {
            'status': 'warning',
            'message': 'No new tweets after filtering recent duplicates',
        }

    logger.info(f"Preview ready: {len(top)} candidates from {source}")
    return {
        'status': 'success',
        'source': source,
        'tweets': top,
    }


async def commit_tweets(tweets: List[Dict]) -> Dict:
    """
    Commit approved tweets as KeyTweet records (stage 2 of approval flow).

    Deactivates old targets and creates new ones from the approved list.

    Args:
        tweets: List of tweet dicts approved by the admin

    Returns:
        Dict with deactivated/created counts
    """
    from apps.tasks.models import Task, KeyTweet

    task = await sync_to_async(
        lambda: Task.objects.filter(task_type='twitter_comment', is_active=True).first()
    )()

    if not task:
        return {'status': 'error', 'message': 'No active twitter_comment task'}

    # Deactivate old targets
    deactivated = await sync_to_async(
        lambda: KeyTweet.objects.filter(task=task, is_active=True).update(is_active=False)
    )()

    # Create new KeyTweet records
    for order_idx, tweet in enumerate(tweets):
        await sync_to_async(KeyTweet.objects.create)(
            task=task,
            tweet_url=tweet['url'],
            author_name=tweet.get('author_name', 'Unknown')[:200],
            author_handle=tweet.get('author_handle', '@unknown')[:100],
            description=tweet.get('text', '')[:200],
            order=order_idx,
            is_active=True,
        )

    logger.info(
        f"Committed {len(tweets)} tweets (deactivated {deactivated} old)"
    )

    return {
        'status': 'success',
        'deactivated': deactivated,
        'created': len(tweets),
        'tweets': tweets,
    }


async def discover_top_tweets(count: int = 20) -> Dict:
    """
    Full pipeline: preview + commit in one call (for backward compat).
    Used only by the auto-scheduler when no admin is available.
    """
    result = await preview_tweets(count=count)
    if result.get('status') != 'success':
        return result

    commit_result = await commit_tweets(result['tweets'])
    commit_result['source'] = result.get('source', 'unknown')
    return commit_result


def format_channel_message(tweets: List[Dict]) -> str:
    """Format the daily channel post with top engagement targets."""
    msg = "🎯 <b>Today's Engagement Targets</b>\n\n"
    msg += (
        "Reply to these tweets to amplify the message "
        "for the 168 children of Minab:\n\n"
    )

    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    # Show top 5 in the channel post
    for idx, tweet in enumerate(tweets[:5]):
        emoji = emojis[idx] if idx < 5 else f"{idx + 1}."
        text_preview = tweet.get('text', '')[:80]
        msg += f"{emoji} <b>{tweet.get('author_handle', '')}</b>\n"
        if text_preview:
            ellipsis = '...' if len(tweet.get('text', '')) > 80 else ''
            msg += f"   <i>{text_preview}{ellipsis}</i>\n"
        msg += f"   🔗 {tweet['url']}\n\n"

    if len(tweets) > 5:
        msg += f"<i>...and {len(tweets) - 5} more targets available in the bot.</i>\n\n"

    msg += "👉 Open the bot to start: @peopleforpeacebot\n"
    msg += "#JusticeForMinabChildren #168Children"

    return msg
