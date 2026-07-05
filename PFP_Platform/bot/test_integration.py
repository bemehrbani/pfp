#!/usr/bin/env python3
"""
Integration test for Telegram bot with Django.
Tests basic functionality without requiring actual Telegram API.
"""
import os
import sys
import asyncio
import logging
from unittest.mock import Mock, AsyncMock, patch

# Add telegram-bot directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def test_django_setup():
    """Test Django setup without actual database."""
    print("Testing Django setup...")

    try:
        # Mock Django setup to avoid actual database connection
        with patch('django.setup') as mock_setup:
            from bot import PFPCampaignBot

            # Create bot instance (should call _setup_django)
            bot = PFPCampaignBot(token="test_token")

            # Verify Django setup was called
            mock_setup.assert_called_once()
            print("✅ Django setup test passed")
            return True
    except Exception as e:
        print(f"❌ Django setup test failed: {e}")
        return False


def test_handler_import():
    """Test that all handlers can be imported."""
    print("\nTesting handler imports...")

    try:
        # Try to import all handlers
        from handlers import (
            start_command, help_command,
            campaigns_command, tasks_command,
            profile_command, leaderboard_command
        )

        print("✅ Handler import test passed")
        return True
    except ImportError as e:
        print(f"❌ Handler import test failed: {e}")
        return False


def test_utility_modules():
    """Test utility module imports and basic functionality."""
    print("\nTesting utility modules...")

    tests_passed = 0
    total_tests = 3

    try:
        # Test django_integration
        from utils.django_integration import setup_django, is_django_available

        # Mock Django setup
        with patch('django.setup'):
            # Should not raise exception
            setup_django()
            tests_passed += 1
            print("  ✅ django_integration module imports")

    except Exception as e:
        print(f"  ❌ django_integration test failed: {e}")

    try:
        # Test state_management
        from utils.state_management import ConversationStateManager

        # Create instance
        manager = ConversationStateManager()
        tests_passed += 1
        print("  ✅ state_management module imports")

    except Exception as e:
        print(f"  ❌ state_management test failed: {e}")

    try:
        # Test error_handling
        from utils.error_handling import BotError, error_handler

        # Create error instance
        error = BotError("Test error", "User message")
        tests_passed += 1
        print("  ✅ error_handling module imports")

    except Exception as e:
        print(f"  ❌ error_handling test failed: {e}")

    print(f"  📊 Utility modules: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests


async def test_bot_initialization():
    """Test bot initialization and handler registration."""
    print("\nTesting bot initialization...")

    try:
        # Mock telegram.ext imports
        with patch('telegram.ext.Updater'), \
             patch('telegram.ext.CommandHandler'), \
             patch('bot.logger'):

            from bot import PFPCampaignBot

            # Create bot instance
            bot = PFPCampaignBot(token="test_token")

            # Mock dispatcher
            bot.dispatcher = Mock()
            bot.dispatcher.add_handler = Mock()
            bot.dispatcher.add_error_handler = Mock()
            bot.dispatcher.handlers = []

            # Call _init_handlers
            bot._init_handlers()

            # Verify handlers were registered
            assert bot.dispatcher.add_handler.called
            assert bot.dispatcher.add_error_handler.called

            print("✅ Bot initialization test passed")
            return True

    except Exception as e:
        print(f"❌ Bot initialization test failed: {e}")
        return False


def test_handler_functions():
    """Test that handler functions have correct signatures."""
    print("\nTesting handler function signatures...")

    try:
        from handlers import (
            start_command, help_command,
            campaigns_command, tasks_command
        )

        # Check that handlers are async functions
        assert asyncio.iscoroutinefunction(start_command)
        assert asyncio.iscoroutinefunction(help_command)
        assert asyncio.iscoroutinefunction(campaigns_command)
        assert asyncio.iscoroutinefunction(tasks_command)

        print("✅ Handler function signature test passed")
        return True

    except Exception as e:
        print(f"❌ Handler function signature test failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("Running Telegram Bot Integration Tests")
    print("=" * 60)

    results = []

    # Run synchronous tests
    results.append(test_django_setup())
    results.append(test_handler_import())
    results.append(test_utility_modules())
    results.append(test_handler_functions())

    # Run async test
    try:
        result = asyncio.run(test_bot_initialization())
        results.append(result)
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)