import logging
import json
import os
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

from apps.tasks.models import Task
from django.db.models import Q


@sync_to_async
def _get_protest_events():
    """Fetch verified upcoming global protests from the database."""
    try:
        from apps.campaigns.models import ProtestEvent
        from django.utils import timezone
        
        events = ProtestEvent.objects.filter(
            is_verified=True,
            event_datetime__gte=timezone.now() - timezone.timedelta(days=1)
        ).order_by('event_datetime')[:15]
        
        results = []
        for e in events:
            date_str = e.event_datetime.strftime('%Y-%m-%d') if e.event_datetime else '-'
            time_str = e.event_datetime.strftime('%H:%M') if e.event_datetime else '-'
            city = e.city or '-'
            country = e.country or ''
            
            results.append({
                "city": city,
                "country": country,
                "date": date_str,
                "time": time_str,
                "topic": e.topic or 'Global Solidarity',
                "details": str(e.title)
            })
        return results
    except Exception as e:
        logger.error(f"Error fetching protests from DB: {e}")
        return []


@sync_to_async
def _get_platform_targets(platform: str, lang: str = 'en'):
    """Fetch active target descriptions and URLs from DB."""
    # Fetch active tasks mapped to an active campaign
    base_qs = Task.objects.filter(is_active=True, campaign__status='active')
    
    tasks = []
    if platform == 'twitter':
        tasks = base_qs.filter(
            Q(target_url__icontains='twitter.com') | 
            Q(target_url__icontains='x.com') |
            Q(task_type__startswith='twitter_')
        ).exclude(target_url='')
    elif platform == 'insta':
        tasks = base_qs.filter(target_url__icontains='instagram.com').exclude(target_url='')
        
    results = []
    # Limit to 5 so we don't overflow the keyboard
    for t in tasks.order_by('-created_at')[:5]:
        results.append({
            "id": t.id,
            "name": t.localized_title(lang),
            "url": t.target_url
        })
    return results

@sync_to_async
def _get_task_url(task_id: int):
    try:
        return Task.objects.get(id=task_id).target_url
    except Task.DoesNotExist:
        return ""


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
        [InlineKeyboardButton(t('simplified_btn_protests', lang), callback_data="simp_protests_menu")],
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
        [InlineKeyboardButton(t('simplified_btn_protests', lang), callback_data="simp_protests_menu")],
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
    
    targets_data = await _get_platform_targets(platform, lang)
    
    if platform == "twitter":
        text = t('simplified_twitter_targets', lang)
        for target in targets_data:
            keyboard.append([InlineKeyboardButton(f"🎯 {target['name']}", callback_data=f"simp_target_twitter_{target['id']}")])
    elif platform == "insta":
        text = t('simplified_instagram_targets', lang)
        for target in targets_data:
            keyboard.append([InlineKeyboardButton(f"📸 {target['name']}", callback_data=f"simp_target_insta_{target['id']}")])
        
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
    # Callback: simp_target_twitter_5
    parts = query.data.split('_')
    platform = parts[-2]
    task_id = int(parts[-1])
    
    # Default to English comment view
    text = t('simplified_comment_en', lang)
    
    # Check if target URL exists before trying to access it
    url = await _get_task_url(task_id)
    
    keyboard = [
        [
            InlineKeyboardButton(t('simplified_btn_get_en', lang), callback_data=f"simp_comment_en_{platform}_{task_id}"),
            InlineKeyboardButton(t('simplified_btn_get_fa', lang), callback_data=f"simp_comment_fa_{platform}_{task_id}")
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
    # simp_comment_fa_twitter_5
    comment_lang = parts[2]
    platform = parts[3]
    task_id = int(parts[4])
    
    if comment_lang == "fa":
        text = t('simplified_comment_fa', lang)
    else:
        text = t('simplified_comment_en', lang)
        
    url = await _get_task_url(task_id)
         
    keyboard = [
        [
            InlineKeyboardButton(t('simplified_btn_get_en', lang), callback_data=f"simp_comment_en_{platform}_{task_id}"),
            InlineKeyboardButton(t('simplified_btn_get_fa', lang), callback_data=f"simp_comment_fa_{platform}_{task_id}")
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


async def simp_handle_protests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle protests submenu: list events or submit a new notice."""
    query = update.callback_query
    await query.answer()

    session, _ = await state_manager.get_or_create_session(update, context)
    lang = getattr(session, 'language', 'en') or 'en'

    action = query.data

    if action == "simp_protests_menu":
        keyboard = [
            [InlineKeyboardButton(t('simplified_btn_protests_list', lang), callback_data="simp_protests_list")],
            [InlineKeyboardButton(t('simplified_btn_protests_share', lang), callback_data="simp_protests_submit")],
            [InlineKeyboardButton("🔙 Back", callback_data="simp_start_task")],
        ]
        await query.edit_message_text(
            text=t('simplified_protests_menu_title', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
        )
        return

    if action == "simp_protests_list":
        events = await _get_protest_events()
        if not events:
            text = t('simplified_protests_list_empty', lang)
        else:
            lines = [t('simplified_protests_list_title', lang), ""]
            for idx, e in enumerate(events, 1):
                city = e.get('city', '-')
                country = e.get('country', '')
                date = e.get('date', '-')
                time_s = e.get('time', '-')
                topic = e.get('topic', 'Iran & Palestine')
                details = e.get('details', '')
                
                loc_str = f"{city}, {country}" if country else city
                lines.append(f"{idx}. 📍 {loc_str}")
                lines.append(f"   🗓 {date}  🕒 {time_s}")
                lines.append(f"   ✊ {topic}")
                if details:
                    lines.append(f"   ℹ️ {details}")
                lines.append("")
            text = "\n".join(lines).strip()

        keyboard = [
            [InlineKeyboardButton(t('simplified_btn_protests_share', lang), callback_data="simp_protests_submit")],
            [InlineKeyboardButton("🔙 Back", callback_data="simp_protests_menu")],
        ]
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
            disable_web_page_preview=True,
        )
        return

    if action == "simp_protests_submit":
        context.user_data['escalation_state'] = 'waiting_for_protest_notice'
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="simp_protests_menu")]]
        await query.edit_message_text(
            text=t('simplified_protests_submit_prompt', lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
        )
        return


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
        text = t('simplified_escalation_creator_prompt', lang)
        context.user_data['escalation_state'] = 'waiting_for_creator_info'
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
    """Catches text messages from users in the escalation flow and forwards them."""
    state = context.user_data.get('escalation_state')
    
    if state in ['waiting_for_submission', 'waiting_for_creator_info', 'waiting_for_protest_notice']:
        session, _ = await state_manager.get_or_create_session(update, context)
        lang = getattr(session, 'language', 'en') or 'en'
        
        # Determine specific text based on state
        if state == 'waiting_for_submission':
            success_msg = "✅ Received! Thank you for your submission. Our team will review it shortly."
            tag = "Account/Text Submission"
        elif state == 'waiting_for_protest_notice':
            success_msg = t('simplified_protests_submit_success', lang)
            tag = "Protest Notice Submission"
        else:
            success_msg = t('simplified_escalation_creator', lang)
            tag = "Creator Portfolio Submission"

        # Forward to admin group
        from asgiref.sync import sync_to_async
        from apps.campaigns.models import Campaign
        
        @sync_to_async
        def _get_active_group_id():
            c = Campaign.objects.filter(status='active').first()
            if c and getattr(c, 'telegram_group_id', None):
                return c.telegram_group_id
            return '-1003589505086' # Fallback to P4P Internal
            
        group_id = await _get_active_group_id()
        
        if group_id:
            try:
                username = update.message.from_user.username or update.message.from_user.first_name
                forward_text = f"🆕 *New {tag}*\n👤 From: @{username}\n📝 Message:\n{update.message.text}"
                await context.bot.send_message(
                    chat_id=group_id,
                    text=forward_text,
                    parse_mode='Markdown'
                )
            except Exception as e:
                import logging
                logging.error(f"Failed to forward submission to admin group: {e}")

        # In a real app context, also save to models.UserSubmission here
        
        await update.message.reply_text(
            success_msg,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Flow", callback_data="simp_done")]])
        )
        context.user_data['escalation_state'] = None


# --- Handlers Export ---
simplified_handlers = [
    CallbackQueryHandler(simp_handle_start_task, pattern=r"^simp_start_task$"),
    CallbackQueryHandler(simp_handle_restart, pattern=r"^simp_restart$"),
    CallbackQueryHandler(simp_handle_protests, pattern=r"^simp_protests_"),
    CallbackQueryHandler(simp_handle_platform, pattern=r"^simp_plat_"),
    CallbackQueryHandler(simp_handle_target, pattern=r"^simp_target_"),
    CallbackQueryHandler(simp_handle_comment_lang, pattern=r"^simp_comment_"),
    CallbackQueryHandler(simp_handle_done, pattern=r"^simp_done$"),
    CallbackQueryHandler(simp_handle_escalation, pattern=r"^simp_escalate_"),
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_submission),
]


