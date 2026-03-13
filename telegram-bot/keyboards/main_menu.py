"""
Inline keyboards for main menu.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    """Create main inline menu keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("📋 Campaigns", callback_data='menu_campaigns'),
            InlineKeyboardButton("🎯 Tasks", callback_data='menu_tasks'),
        ],
        [
            InlineKeyboardButton("📊 Progress", callback_data='menu_progress'),
            InlineKeyboardButton("🏆 Leaderboard", callback_data='menu_leaderboard'),
        ],
        [
            InlineKeyboardButton("👤 Profile", callback_data='menu_profile'),
            InlineKeyboardButton("ℹ️ Help", callback_data='menu_help'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def campaigns_menu_keyboard(campaigns):
    """Create keyboard for campaigns list."""
    keyboard = []
    for campaign in campaigns:
        keyboard.append([
            InlineKeyboardButton(
                f"📍 {campaign['name']}",
                callback_data=f'campaign_{campaign["id"]}'
            )
        ])
    keyboard.append([
        InlineKeyboardButton("⬅️ Back", callback_data='menu_main'),
        InlineKeyboardButton("🔄 Refresh", callback_data='menu_campaigns'),
    ])
    return InlineKeyboardMarkup(keyboard)


def tasks_menu_keyboard(tasks):
    """Create keyboard for tasks list."""
    keyboard = []
    for task in tasks:
        keyboard.append([
            InlineKeyboardButton(
                f"{task['emoji']} {task['title']}",
                callback_data=f'task_{task["id"]}'
            )
        ])
    keyboard.append([
        InlineKeyboardButton("⬅️ Back", callback_data='menu_main'),
        InlineKeyboardButton("🔄 Refresh", callback_data='menu_tasks'),
    ])
    return InlineKeyboardMarkup(keyboard)


def task_detail_keyboard(task_id, can_claim=True):
    """Create keyboard for task details."""
    keyboard = []
    if can_claim:
        keyboard.append([
            InlineKeyboardButton("✅ Claim Task", callback_data=f'claim_{task_id}')
        ])
    keyboard.append([
        InlineKeyboardButton("⬅️ Back to Tasks", callback_data='menu_tasks'),
        InlineKeyboardButton("📋 View Campaign", callback_data=f'campaign_from_task_{task_id}'),
    ])
    return InlineKeyboardMarkup(keyboard)


def confirmation_keyboard(action, item_id):
    """Create confirmation keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data=f'confirm_{action}_{item_id}'),
            InlineKeyboardButton("❌ No", callback_data=f'cancel_{action}_{item_id}'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)