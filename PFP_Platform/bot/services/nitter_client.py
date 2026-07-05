"""
Nitter RSS client for tweet discovery.

Fetches tweets from Nitter's public RSS feeds (free, no authentication).
Supports both search queries and individual account monitoring.
Multiple Nitter instances are tried for redundancy.

Monitored accounts are stored in a JSON file so they can be managed via
bot commands (/add_account, /remove_account) without redeploying.
"""
import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import quote

import aiohttp

logger = logging.getLogger(__name__)

# ── Nitter instances (tried in order) ───────────────────────────
NITTER_INSTANCES = [
    'https://nitter.poast.org',
    'https://nitter.privacydev.net',
    'https://nitter.woodland.cafe',
    'https://nitter.net',
    'https://nitter.cz',
    'https://nitter.1d4.us',
    'https://nitter.kavin.rocks',
]

# ── Campaign search queries (broader) ───────────────────────────
SEARCH_QUERIES = [
    '#JusticeForMinabChildren',
    '#168Children',
    '#StopTheWar Iran',
    '#CeasefireNow Iran',
    '#HandsOffIran',
    '#ProtectCivilians Iran',
    '#PeopleForPeace',
    'Minab school',
    'Minab airstrike',
    'Iran children killed',
    'Iran children war crime',
    'Iran US aggression children',
    'Iran school bombing',
    'Iran civilians bombing',
    'Iran peace children',
    'Iran war children',
    'Iran cruise missile',
    'Iran airstrike school',
]

# ── Default priority accounts ──────────────────────────────────
DEFAULT_PRIORITY_ACCOUNTS = [
    'KenRoth',
    'mbaborak',
    'christaborger',
    'TritaParsi',
    'SinaToossi',
    'AssalRad',
    'NIACouncil',
    'UNGeneva',
    'amnesty',
    'hrw',
    'UNHumanRights',
    'ABORDEAUX2',
    'JavierBlas',
    'claraborja',
    'Reuters',
    'AP',
    'BBCWorld',
    'AJEnglish',
    'taborender',
    'PressTV',
    'UNICEF',
    'JavadZarif',
]

# Exported as the canonical list (built later by _load_accounts)
PRIORITY_ACCOUNTS: List[str] = list(DEFAULT_PRIORITY_ACCOUNTS)

# ── Persistent account storage ──────────────────────────────────
_DATA_DIR = Path(os.getenv('BOT_DATA_DIR', '/app/data'))
_ACCOUNTS_FILE = _DATA_DIR / 'monitored_accounts.json'


def _load_accounts() -> List[str]:
    """Load the list of monitored accounts from disk + defaults."""
    global PRIORITY_ACCOUNTS

    extra: List[str] = []
    if _ACCOUNTS_FILE.exists():
        try:
            with open(_ACCOUNTS_FILE) as fh:
                extra = json.load(fh)
        except (json.JSONDecodeError, OSError):
            extra = []

    # Merge default + user-added, deduplicate while preserving order
    seen: Set[str] = set()
    merged: List[str] = []
    for handle in list(DEFAULT_PRIORITY_ACCOUNTS) + extra:
        clean = handle.lstrip('@')
        if clean not in seen:
            seen.add(clean)
            merged.append(clean)

    PRIORITY_ACCOUNTS.clear()
    PRIORITY_ACCOUNTS.extend(merged)
    return merged


def _save_custom_accounts(accounts: List[str]) -> None:
    """Save user-added accounts to disk."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(_ACCOUNTS_FILE, 'w') as fh:
        json.dump(accounts, fh, indent=2)


def add_monitored_account(handle: str) -> bool:
    """Add a Twitter account to the monitored list. Returns True if new."""
    clean = handle.lstrip('@')
    _load_accounts()

    if clean in PRIORITY_ACCOUNTS:
        return False

    # Load custom-only list
    custom: List[str] = []
    if _ACCOUNTS_FILE.exists():
        try:
            with open(_ACCOUNTS_FILE) as fh:
                custom = json.load(fh)
        except (json.JSONDecodeError, OSError):
            custom = []

    custom.append(clean)
    _save_custom_accounts(custom)
    _load_accounts()
    return True


def remove_monitored_account(handle: str) -> bool:
    """Remove a Twitter account from the monitored list. Returns True if removed."""
    clean = handle.lstrip('@')

    # Only remove from custom list (can't remove defaults via command)
    custom: List[str] = []
    if _ACCOUNTS_FILE.exists():
        try:
            with open(_ACCOUNTS_FILE) as fh:
                custom = json.load(fh)
        except (json.JSONDecodeError, OSError):
            custom = []

    if clean not in custom and clean not in DEFAULT_PRIORITY_ACCOUNTS:
        return False

    custom = [a for a in custom if a != clean]
    _save_custom_accounts(custom)
    _load_accounts()
    return True


def get_monitored_accounts() -> Dict[str, List[str]]:
    """Return categorized monitored accounts."""
    custom: List[str] = []
    if _ACCOUNTS_FILE.exists():
        try:
            with open(_ACCOUNTS_FILE) as fh:
                custom = json.load(fh)
        except (json.JSONDecodeError, OSError):
            custom = []

    return {
        'default': list(DEFAULT_PRIORITY_ACCOUNTS),
        'custom': custom,
        'all': list(PRIORITY_ACCOUNTS),
    }


# ── Relevance keywords (for filtering account feeds) ────────────
RELEVANCE_KEYWORDS = [
    'minab', '168 children', 'iran children', 'iran school',
    'war crime', 'airstrike', 'justiceforminab', 'stopthewar',
    'iran aggression', 'iran bombing', 'ceasefire', 'peace iran',
    'iran war', 'children killed', 'school attack', 'civilian',
    'children', 'iran', 'missile', 'sanctions', 'peace',
    'bombing', 'war', 'attack', 'killed',
]


async def fetch_search_rss(query: str, instance: str) -> List[Dict]:
    """Fetch tweets from a Nitter search RSS feed."""
    encoded_query = quote(query, safe='')
    url = f"{instance}/search/rss?f=tweets&q={encoded_query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=15),
                headers={'User-Agent': 'Mozilla/5.0 PFP-Bot/1.0'},
            ) as resp:
                if resp.status != 200:
                    logger.warning(f"Nitter search failed: {url} → HTTP {resp.status}")
                    return []
                xml_text = await resp.text()
    except (aiohttp.ClientError, TimeoutError) as exc:
        logger.warning(f"Nitter request error for {url}: {exc}")
        return []

    return _parse_rss(xml_text, instance)


async def fetch_account_rss(handle: str, instance: str) -> List[Dict]:
    """Fetch recent tweets from a specific account's RSS feed."""
    url = f"{instance}/{handle}/rss"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=15),
                headers={'User-Agent': 'Mozilla/5.0 PFP-Bot/1.0'},
            ) as resp:
                if resp.status != 200:
                    logger.warning(f"Nitter account feed failed: {url} → HTTP {resp.status}")
                    return []
                xml_text = await resp.text()
    except (aiohttp.ClientError, TimeoutError) as exc:
        logger.warning(f"Nitter account request error for {url}: {exc}")
        return []

    return _parse_rss(xml_text, instance)


def _parse_rss(xml_text: str, instance: str) -> List[Dict]:
    """Parse Nitter RSS XML into tweet dicts."""
    tweets = []
    try:
        root = ET.fromstring(xml_text)
        for item in root.findall('.//item'):
            title = item.findtext('title', '')
            link = item.findtext('link', '')
            pub_date = item.findtext('pubDate', '')
            description = item.findtext('description', '')

            tweet_url = _nitter_to_twitter_url(link, instance)
            if not tweet_url:
                continue

            handle_match = re.search(r'x\.com/(\w+)/status/', tweet_url)
            handle = f"@{handle_match.group(1)}" if handle_match else '@unknown'

            # Strip HTML tags from description
            clean_text = re.sub(r'<[^>]+>', '', description).strip()

            # Extract author name from title ("Author: tweet text...")
            author_name = title.split(':')[0].strip() if ':' in title else handle.lstrip('@')

            tweets.append({
                'url': tweet_url,
                'author_name': author_name,
                'author_handle': handle,
                'text': clean_text[:300],
                'pub_date': pub_date,
            })
    except ET.ParseError:
        logger.error("Failed to parse Nitter RSS XML")

    return tweets


def _nitter_to_twitter_url(nitter_url: str, instance: str) -> str:
    """Convert a Nitter URL to a canonical x.com URL."""
    if not nitter_url:
        return ''
    domain = instance.replace('https://', '').replace('http://', '')
    return nitter_url.replace(domain, 'x.com')


def _is_relevant(text: str) -> bool:
    """Check if a tweet text is relevant to the campaign."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in RELEVANCE_KEYWORDS)


async def fetch_all_tweets() -> List[Dict]:
    """
    Fetch tweets from all search queries and priority accounts.
    Tries multiple Nitter instances for redundancy.

    Returns:
        List of tweet dicts with keys: url, author_name, author_handle, text, pub_date
    """
    # Reload accounts from disk (picks up /add_account changes)
    _load_accounts()

    all_tweets: List[Dict] = []

    for instance in NITTER_INSTANCES:
        try:
            # Search queries
            for query in SEARCH_QUERIES:
                tweets = await fetch_search_rss(query, instance)
                all_tweets.extend(tweets)

            # Priority account feeds (only relevant tweets)
            for handle in PRIORITY_ACCOUNTS:
                tweets = await fetch_account_rss(handle, instance)
                relevant = [t for t in tweets if _is_relevant(t['text'])]
                all_tweets.extend(relevant)

            if all_tweets:
                logger.info(f"Nitter: fetched {len(all_tweets)} tweets from {instance}")
                break

        except Exception as exc:
            logger.warning(f"Nitter instance {instance} failed entirely: {exc}")
            continue

    return all_tweets


# Load accounts on module import
_load_accounts()
