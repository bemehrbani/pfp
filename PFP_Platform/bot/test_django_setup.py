#!/usr/bin/env python3
"""
Test Django setup for Telegram bot.
"""
import os
import sys
import logging

# Set environment variables for development
os.environ['DATABASE_URL'] = 'postgres://pfp_user:pfp_password@localhost:5432/pfp_campaign'
os.environ['REDIS_URL'] = 'redis://localhost:6379/0'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import bot class
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from bot import PFPCampaignBot
    print("✅ Successfully imported PFPCampaignBot")
except ImportError as e:
    print(f"❌ Failed to import PFPCampaignBot: {e}")
    sys.exit(1)

# Test Django setup
try:
    # Create bot instance with dummy token
    bot = PFPCampaignBot(token='dummy_token')
    print("✅ Bot instance created successfully")

    # Try to access a Django model to verify integration
    from django.apps import apps
    from apps.users.models import User
    print("✅ Django models can be imported")

    # Try a simple query (may fail due to missing DB, but should not raise ImportError)
    user_count = User.objects.count()
    print(f"✅ Database query successful (user count: {user_count})")

    print("\n🎉 Django integration test PASSED!")
    sys.exit(0)

except Exception as e:
    print(f"❌ Django integration test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)