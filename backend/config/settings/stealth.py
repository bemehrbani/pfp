"""
Stealth mode settings for PFP Campaign Manager.
Production-grade but accessible over HTTP via IP (no domain/SSL).
"""
from .production import *

# Disable SSL requirements for IP-only access
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CSRF trusted origins — required by Django 4.x for admin login behind reverse proxy
CSRF_TRUSTED_ORIGINS = [
    'https://peopleforpeace.live',
    'http://peopleforpeace.live',
    'http://65.109.198.200:8080',
    'http://65.109.198.200:8001',
]

# Telegram stays in polling mode (no webhook without domain)
TELEGRAM_USE_WEBHOOK = False
