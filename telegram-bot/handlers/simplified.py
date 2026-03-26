import logging
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from utils.state_management import state_manager
from utils.translations import t

logger = logging.getLogger(__name__)

# --- State Constants ---
# Kept internal to this module, though they could be integrated into a larger ConversationHandler
PLATFORM_PICKER = 1
TARGETS = 2
COMMENT = 3
ESCALATION = 4

# --- Target Data (Hardcoded for prototype parity) ---
TWITTER_TARGETS = [
    {
        "name": "UNICEF Iran",
        "url": "https://x.com/UNICEF_IRAN/status/1897290076295536768",
        "description": "Demand official investigation"
    },
    {
        "name": "Amnesty Iran",
        "url": "https://x.com/AmnestyIran/status/1897354972106363294",
        "description": "Amplify local reports"
    },
    {
        "name": "Human Rights Watch",
        "url": "https://x.com/hrw/status/1897371994018046039",
        "description": "Call for international action"
    }
]

INSTAGRAM_TARGETS = [
    {
        "name": "UNICEF Iran",
        "url": "https://www.instagram.com/unicef_iran/p/123456789/",
        "description": "Demand official investigation"
    },
    {
        "name": "Amnesty Iran",
        "url": "https://www.instagram.com/amnestyiran/p/123456789/",
        "description": "Amplify local reports"
    }
]


async def process_start_simplified(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Entry point for the unified single-task flow.
    Invoked directly from start.py when a registered user types /start.
    """
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    
    welcome_text = t('simplified_welcome', lang)
    
    keyboard = [
        [InlineKeyboardButton(t('simplified_btn_start', lang), callback_data="simp_start_task")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def simp_handle_start_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the platform picker."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    
    keyboard = [
        [InlineKeyboardButton(t('simplified_btn_twitter', lang), callback_data="simp_plat_twitter")],
        [InlineKeyboardButton(t('simplified_btn_instagram', lang), callback_data="simp_plat_insta")],
        [InlineKeyboardButton(t('simplified_btn_creator', lang), callback_data="simp_escalate_creator")],
        [InlineKeyboardButton(t('simplified_btn_invite', lang), callback_data="simp_escalate_invite")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=t('simplified_platform_picker', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def simp_handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes the current message (e.g. video) and sends the platform picker."""
    query = update.callback_query
    await query.answer()
    
    try:
        await query.delete_message()
    except Exception:
        pass
        
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    
    keyboard = [
        [InlineKeyboardButton(t('simplified_btn_twitter', lang), callback_data="simp_plat_twitter")],
        [InlineKeyboardButton(t('simplified_btn_instagram', lang), callback_data="simp_plat_insta")],
        [InlineKeyboardButton(t('simplified_btn_creator', lang), callback_data="simp_escalate_creator")],
        [InlineKeyboardButton(t('simplified_btn_invite', lang), callback_data="simp_escalate_invite")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.get_bot().send_message(
        chat_id=query.message.chat_id,
        text=t('simplified_platform_picker', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def simp_handle_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows targets for the selected platform."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    platform = query.data.split('_')[-1]
    
    keyboard = []
    
    if platform == "twitter":
        text = t('simplified_twitter_targets', lang)
        for i, target in enumerate(TWITTER_TARGETS):
            # Pass index in callback data to reference target later
            keyboard.append([InlineKeyboardButton(f"🎯 {target['name']}", callback_data=f"simp_target_twitter_{i}")])
    elif platform == "insta":
        text = t('simplified_instagram_targets', lang) # Assuming fallback or similar text
        for i, target in enumerate(INSTAGRAM_TARGETS):
            keyboard.append([InlineKeyboardButton(f"📸 {target['name']}", callback_data=f"simp_target_insta_{i}")])
        
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="simp_start_task")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


async def simp_handle_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the comment template and logic to switch languages."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    
    # Parse which platform and target was clicked
    # Callback: simp_target_twitter_0
    parts = query.data.split('_')
    platform = parts[-2]
    target_idx = int(parts[-1])
    
    # Default to English comment view
    text = t('simplified_comment_en', lang)
    
    # Check if target URL exists before trying to access it
    url = ""
    if platform == "twitter" and target_idx < len(TWITTER_TARGETS):
         url = TWITTER_TARGETS[target_idx]["url"]
    elif platform == "insta" and target_idx < len(INSTAGRAM_TARGETS):
         url = INSTAGRAM_TARGETS[target_idx]["url"]
    
    keyboard = [
        [
            InlineKeyboardButton(t('simplified_btn_get_en', lang), callback_data=f"simp_comment_en_{platform}_{target_idx}"),
            InlineKeyboardButton(t('simplified_btn_get_fa', lang), callback_data=f"simp_comment_fa_{platform}_{target_idx}")
        ],
        [InlineKeyboardButton("💬 Go to Post", url=url)] if url else [],
        [InlineKeyboardButton(t('simplified_btn_done', lang), callback_data="simp_done")],
        [InlineKeyboardButton("🔙 Back to Targets", callback_data=f"simp_plat_{platform}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


async def simp_handle_comment_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Updates the comment text to the selected language."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    parts = query.data.split('_')
    # simp_comment_fa_twitter_0
    comment_lang = parts[2]
    platform = parts[3]
    target_idx = int(parts[4])
    
    if comment_lang == "fa":
        text = t('simplified_comment_fa', lang)
    else:
        text = t('simplified_comment_en', lang)
        
    url = ""
    if platform == "twitter" and target_idx < len(TWITTER_TARGETS):
         url = TWITTER_TARGETS[target_idx]["url"]
    elif platform == "insta" and target_idx < len(INSTAGRAM_TARGETS):
         url = INSTAGRAM_TARGETS[target_idx]["url"]
         
    keyboard = [
        [
            InlineKeyboardButton(t('simplified_btn_get_en', lang), callback_data=f"simp_comment_en_{platform}_{target_idx}"),
            InlineKeyboardButton(t('simplified_btn_get_fa', lang), callback_data=f"simp_comment_fa_{platform}_{target_idx}")
        ],
        [InlineKeyboardButton("💬 Go to Post", url=url)] if url else [],
        [InlineKeyboardButton(t('simplified_btn_done', lang), callback_data="simp_done")],
        [InlineKeyboardButton("🔙 Back to Targets", callback_data=f"simp_plat_{platform}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass  # User clicked the button for the currently displayed language
        else:
            raise


async def simp_handle_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows the escalation screen after task completion."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    
    text = t('simplified_completion', lang)
    
    keyboard = [
        [InlineKeyboardButton(t('simplified_btn_another_platform', lang), callback_data="simp_start_task")],
        [InlineKeyboardButton(t('simplified_btn_submit_content', lang), callback_data="simp_escalate_submit")],
        [InlineKeyboardButton(t('simplified_btn_creator', lang), callback_data="simp_escalate_creator")],
        [InlineKeyboardButton(t('simplified_btn_invite', lang), callback_data="simp_escalate_invite")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def simp_handle_escalation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the choices from the escalation screen."""
    query = update.callback_query
    await query.answer()
    
    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'
    action = query.data.split('_')[-1]
    
    if action == "submit":
        text = t('simplified_escalation_submit', lang)
        # Using context.user_data to track state for receiving the message
        context.user_data['escalation_state'] = 'waiting_for_submission'
    elif action == "creator":
        text = t('simplified_escalation_creator', lang)
        context.user_data['escalation_state'] = None
    elif action == "invite":
        context.user_data['escalation_state'] = None
        # Send video directly and return early
        import pathlib
        import os
        
        user_id = session.user.id if session.user else 0
        campaign_id = 1
        invite_link = f"https://t.me/peopleforpeacebot?start=campaign_{campaign_id}_ref_{user_id}"
        
        caption = t('invite_video_caption', lang).format(link=invite_link)
        
        try:
            await query.delete_message()
        except Exception:
            pass

        video_files = {
            'en': '100_faces_FINAL_V3.mp4',
            'fa': '100_faces_FARSI_V1.mp4',
            'ar': '100_faces_ARABIC_V1.mp4',
        }
        assets_dir = os.environ.get('VIDEO_ASSETS_DIR', '/app/assets/videos')
        video_path = pathlib.Path(assets_dir) / video_files.get(lang, video_files['en'])

        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="simp_restart")]]
        
        if not video_path.exists():
            await query.get_bot().send_message(
                chat_id=query.message.chat_id,
                text="❌ Video file not found. Please try again later.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return

        await query.get_bot().send_video(
            chat_id=query.message.chat_id,
            video=open(video_path, 'rb'),
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            supports_streaming=True,
        )
        return
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="simp_done")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_user_submission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Catches text messages from users in the escalation flow."""
    if context.user_data.get('escalation_state') == 'waiting_for_submission':
        session, _ = await state_manager.get_or_create_session(update, context)
        lang = getattr(session, 'language', 'en') or 'en'
        # In a real app, save to models.UserSubmission
        await update.message.reply_text(
            "✅ Received! Thank you for your submission. Our team will review it shortly.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Flow", callback_data="simp_done")]])
        )
        context.user_data['escalation_state'] = None


# --- Handlers Export ---
simplified_handlers = [
    CallbackQueryHandler(simp_handle_start_task, pattern=r"^simp_start_task$"),
    CallbackQueryHandler(simp_handle_restart, pattern=r"^simp_restart$"),
    CallbackQueryHandler(simp_handle_platform, pattern=r"^simp_plat_"),
    CallbackQueryHandler(simp_handle_target, pattern=r"^simp_target_"),
    CallbackQueryHandler(simp_handle_comment_lang, pattern=r"^simp_comment_"),
    CallbackQueryHandler(simp_handle_done, pattern=r"^simp_done$"),
    CallbackQueryHandler(simp_handle_escalation, pattern=r"^simp_escalate_"),
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_submission),
]


