"""
Apify Twitter Scraper fallback client.

Used when all Nitter instances are unreachable.
Uses Apify's free $5/mo credits to run Twitter search actors.
Requires APIFY_TOKEN environment variable.
"""
import logging
import os
from typing import List, Dict

import aiohttp

logger = logging.getLogger(__name__)

APIFY_TOKEN = os.getenv('APIFY_TOKEN', '')
# The actor ID may change — use the current best Twitter scraper on Apify
APIFY_ACTOR_ID = 'apidojo/tweet-scraper'


async def search_tweets_apify(query: str, max_tweets: int = 50) -> List[Dict]:
    """
    Search tweets using Apify's Twitter Scraper actor.

    Args:
        query: Search term (hashtag or keyword)
        max_tweets: Maximum number of tweets to return

    Returns:
        List of tweet dicts with standardised keys
    """
    if not APIFY_TOKEN:
        logger.warning("APIFY_TOKEN not set — skipping Apify fallback")
        return []

    run_url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/run-sync-get-dataset-items"
    headers = {
        'Authorization': f'Bearer {APIFY_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'searchTerms': [query],
        'maxTweets': max_tweets,
        'sort': 'Latest',
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                run_url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=120),
            ) as resp:
                if resp.status != 200:
                    logger.error(f"Apify actor failed: HTTP {resp.status}")
                    return []
                items = await resp.json()
    except (aiohttp.ClientError, TimeoutError) as exc:
        logger.error(f"Apify request error: {exc}")
        return []

    tweets: List[Dict] = []
    for item in items:
        tweet_url = item.get('url', '')
        if 'x.com' not in tweet_url and 'twitter.com' not in tweet_url:
            continue

        author = item.get('author', {})
        tweets.append({
            'url': tweet_url,
            'author_name': author.get('name', ''),
            'author_handle': f"@{author.get('userName', 'unknown')}",
            'text': item.get('text', '')[:300],
            'retweet_count': item.get('retweetCount', 0),
            'like_count': item.get('likeCount', 0),
            'reply_count': item.get('replyCount', 0),
            'quote_count': item.get('quoteCount', 0),
            'follower_count': author.get('followers', 0),
            'pub_date': item.get('createdAt', ''),
        })

    return tweets


async def fetch_all_tweets_apify() -> List[Dict]:
    """
    Search all campaign queries using Apify.
    Only searches the top 3 queries to conserve free credits.
    """
    from .nitter_client import SEARCH_QUERIES

    all_tweets: List[Dict] = []
    # Limit to top 3 queries to save Apify credits ($5 free/mo)
    for query in SEARCH_QUERIES[:3]:
        tweets = await search_tweets_apify(query, max_tweets=30)
        all_tweets.extend(tweets)

    logger.info(f"Apify fallback: fetched {len(all_tweets)} tweets")
    return all_tweets
