"""
Translations for PFP Telegram Bot.
Supports: English (en), Farsi (fa), Arabic (ar).
"""

TRANSLATIONS = {
    # ── Language Picker ──────────────────────────────────────────────
    "choose_language": {
        "en": "🌍 Choose your language:",
        "fa": "🌍 زبان خود را انتخاب کنید:",
        "ar": "🌍 اختر لغتك:",
    },
    "language_set": {
        "en": "✅ Language set to *English*.",
        "fa": "✅ زبان به *فارسی* تغییر کرد.",
        "ar": "✅ تم تعيين اللغة إلى *العربية*.",
    },

    # ── Welcome & Start ──────────────────────────────────────────────
    "welcome": {
        "en": (
            "✊ *People for Peace*\n\n"
            "Choose a campaign below and start taking action!"
        ),
        "fa": (
            "✊ *مردم برای صلح*\n\n"
            "یک کمپین انتخاب کنید و شروع کنید!"
        ),
        "ar": (
            "✊ *الناس من أجل السلام*\n\n"
            "اختر حملة أدناه وابدأ العمل!"
        ),
    },

    # ── Keyboard Buttons ─────────────────────────────────────────────
    "btn_campaigns": {
        "en": "📋 Browse Campaigns",
        "fa": "📋 مرور کمپین‌ها",
        "ar": "📋 تصفح الحملات",
    },
    "btn_my_campaigns": {
        "en": "✊ My Campaigns",
        "fa": "✊ کمپین‌های من",
        "ar": "✊ حملاتي",
    },
    "btn_tasks": {
        "en": "🎯 Available Tasks",
        "fa": "🎯 وظایف موجود",
        "ar": "🎯 المهام المتاحة",
    },
    "btn_progress": {
        "en": "📊 My Progress",
        "fa": "📊 پیشرفت من",
        "ar": "📊 تقدمي",
    },
    "btn_leaderboard": {
        "en": "🏆 Leaderboard",
        "fa": "🏆 جدول امتیازات",
        "ar": "🏆 لوحة المتصدرين",
    },
    "btn_help": {
        "en": "ℹ️ Help",
        "fa": "ℹ️ راهنما",
        "ar": "ℹ️ مساعدة",
    },
    "btn_profile": {
        "en": "👤 Profile",
        "fa": "👤 پروفایل",
        "ar": "👤 الملف الشخصي",
    },
    "btn_language": {
        "en": "🌍 Language",
        "fa": "🌍 زبان",
        "ar": "🌍 اللغة",
    },

    # ── Registration ─────────────────────────────────────────────────
    "register_new_user": {
        "en": "It looks like you're new here! Let's get you registered.\n\nPlease send me your full name to continue.",
        "fa": "به نظر می‌رسد شما تازه‌وارد هستید! بیایید ثبت‌نام کنیم.\n\nلطفاً نام کامل خود را ارسال کنید.",
        "ar": "يبدو أنك جديد هنا! دعنا نسجلك.\n\nيرجى إرسال اسمك الكامل للمتابعة.",
    },
    "register_need_first": {
        "en": "⚠️ You need to register first! Use /start to begin registration.",
        "fa": "⚠️ ابتدا باید ثبت‌نام کنید! از /start استفاده کنید.",
        "ar": "⚠️ يجب عليك التسجيل أولاً! استخدم /start لبدء التسجيل.",
    },
    "register_for_campaign": {
        "en": "You're joining *{name}*! 🕊️\n\nPlease send me your full name to register.",
        "fa": "شما دارید به *{name}* می‌پیوندید! 🕊️\n\nلطفاً نام کامل خود را ارسال کنید.",
        "ar": "أنت تنضم إلى *{name}*! 🕊️\n\nيرجى إرسال اسمك الكامل للتسجيل.",
    },
    "register_name_invalid": {
        "en": "❌ Please enter a valid name (at least 2 characters).",
        "fa": "❌ لطفاً یک نام معتبر وارد کنید (حداقل ۲ حرف).",
        "ar": "❌ يرجى إدخال اسم صالح (حرفان على الأقل).",
    },
    "register_success": {
        "en": (
            "🎉 *Registration Complete!*\n\n"
            "Welcome to People for Peace, {name}! ✌️\n\n"
            "You're all set. Let me show you available campaigns..."
        ),
        "fa": (
            "🎉 *ثبت‌نام کامل شد!*\n\n"
            "به مردم برای صلح خوش آمدید، {name}! ✌️\n\n"
            "همه چیز آماده‌ست. بذار کمپین‌ها رو بهت نشون بدم..."
        ),
        "ar": (
            "🎉 *اكتمل التسجيل!*\n\n"
            "مرحباً في الناس من أجل السلام، {name}! ✌️\n\n"
            "كل شيء جاهز. دعني أعرض لك الحملات المتاحة..."
        ),
    },
    "register_error": {
        "en": "❌ Failed to create account. Please try again with /start.",
        "fa": "❌ ساخت حساب ناموفق بود. لطفاً با /start دوباره امتحان کنید.",
        "ar": "❌ فشل إنشاء الحساب. يرجى المحاولة مرة أخرى باستخدام /start.",
    },
    "auto_joined_campaign": {
        "en": (
            "🎉 *You've joined {name}!*\n\n"
            "{description}\n\n"
            "👥 Members: {members}/{target}\n"
            "🎯 Tasks: {tasks} available\n\n"
            "Tap a task below to get started!"
        ),
        "fa": (
            "🎉 *شما به {name} پیوستید!*\n\n"
            "{description}\n\n"
            "👥 اعضا: {members}/{target}\n"
            "🎯 وظایف: {tasks} موجود\n\n"
            "روی یک وظیفه بزنید تا شروع کنید!"
        ),
        "ar": (
            "🎉 *لقد انضممت إلى {name}!*\n\n"
            "{description}\n\n"
            "👥 الأعضاء: {members}/{target}\n"
            "🎯 المهام: {tasks} متاح\n\n"
            "اضغط على مهمة أدناه للبدء!"
        ),
    },

    # ── Campaigns ─────────────────────────────────────────────────────
    "campaigns_title": {
        "en": "📋 *Available Campaigns*",
        "fa": "📋 *کمپین‌های فعال*",
        "ar": "📋 *الحملات المتاحة*",
    },
    "campaigns_none": {
        "en": "📭 No campaigns available at the moment.",
        "fa": "📭 در حال حاضر کمپینی موجود نیست.",
        "ar": "📭 لا توجد حملات متاحة حالياً.",
    },
    "campaigns_members": {
        "en": "👥 Members",
        "fa": "👥 اعضا",
        "ar": "👥 الأعضاء",
    },
    "campaigns_tasks_available": {
        "en": "🎯 Tasks",
        "fa": "🎯 وظایف",
        "ar": "🎯 المهام",
    },
    "campaigns_available": {
        "en": "available",
        "fa": "موجود",
        "ar": "متاح",
    },
    "campaigns_joined": {
        "en": "✅ Joined",
        "fa": "✅ عضو شدید",
        "ar": "✅ انضممت",
    },
    "btn_view_tasks": {
        "en": "📋 View Tasks",
        "fa": "📋 مشاهده وظایف",
        "ar": "📋 عرض المهام",
    },
    "btn_join": {
        "en": "Join",
        "fa": "عضویت",
        "ar": "انضمام",
    },
    "campaign_joined_success": {
        "en": "🎉 You've successfully joined *{name}*!",
        "fa": "🎉 شما با موفقیت به *{name}* پیوستید!",
        "ar": "🎉 لقد انضممت بنجاح إلى *{name}*!",
    },
    "campaign_not_available": {
        "en": "❌ This campaign is no longer available.",
        "fa": "❌ این کمپین دیگر در دسترس نیست.",
        "ar": "❌ هذه الحملة لم تعد متاحة.",
    },

    # ── Tasks ──────────────────────────────────────────────────────────
    "tasks_title": {
        "en": "🎯 *Tasks for {name}*",
        "fa": "🎯 *وظایف برای {name}*",
        "ar": "🎯 *مهام {name}*",
    },
    "tasks_none": {
        "en": "📭 No tasks available for *{name}* at the moment.",
        "fa": "📭 در حال حاضر وظیفه‌ای برای *{name}* موجود نیست.",
        "ar": "📭 لا توجد مهام متاحة لـ *{name}* حالياً.",
    },
    "tasks_tap_to_start": {
        "en": "Tap a task to see details and start.",
        "fa": "روی یک وظیفه بزنید تا جزئیات را ببینید و شروع کنید.",
        "ar": "اضغط على مهمة لرؤية التفاصيل والبدء.",
    },
    "tasks_not_found": {
        "en": "❌ Task not found.",
        "fa": "❌ وظیفه پیدا نشد.",
        "ar": "❌ لم يتم العثور على المهمة.",
    },

    # ── Task Detail ────────────────────────────────────────────────────
    "task_instructions": {
        "en": "📝 *Instructions:*",
        "fa": "📝 *دستورالعمل:*",
        "ar": "📝 *التعليمات:*",
    },
    "task_hashtags": {
        "en": "#️⃣ *Hashtags:*",
        "fa": "#️⃣ *هشتگ‌ها:*",
        "ar": "#️⃣ *الهاشتاغات:*",
    },
    "task_mentions": {
        "en": "@ *Mentions:*",
        "fa": "@ *منشن‌ها:*",
        "ar": "@ *الإشارات:*",
    },
    "task_link": {
        "en": "🔗 *Link:*",
        "fa": "🔗 *لینک:*",
        "ar": "🔗 *الرابط:*",
    },
    "task_points": {
        "en": "🏆 *Points:*",
        "fa": "🏆 *امتیاز:*",
        "ar": "🏆 *النقاط:*",
    },
    "task_est_time": {
        "en": "⏱ *Est:*",
        "fa": "⏱ *زمان تخمینی:*",
        "ar": "⏱ *الوقت المقدر:*",
    },
    "task_slots": {
        "en": "👥 *Slots:* {n} remaining",
        "fa": "👥 *ظرفیت:* {n} باقیمانده",
        "ar": "👥 *الأماكن:* {n} متبقية",
    },
    "task_pts": {
        "en": "pts",
        "fa": "امتیاز",
        "ar": "نقاط",
    },
    "task_min": {
        "en": "min",
        "fa": "دقیقه",
        "ar": "دقيقة",
    },
    "btn_start_task": {
        "en": "✅ Start This Task",
        "fa": "✅ شروع این وظیفه",
        "ar": "✅ ابدأ هذه المهمة",
    },

    # ── Task Guidance (after starting) ─────────────────────────────────
    "task_started": {
        "en": "🚀 *Task Started!*",
        "fa": "🚀 *وظیفه شروع شد!*",
        "ar": "🚀 *بدأت المهمة!*",
    },
    "tweet_pick_or_write": {
        "en": "📝 *Pick a tweet or write your own:*",
        "fa": "📝 *یک توییت انتخاب کنید یا خودتان بنویسید:*",
        "ar": "📝 *اختر تغريدة أو اكتب واحدة خاصة بك:*",
    },
    "tweet_copy_and_post": {
        "en": "👉 Copy one, customize it & post on Twitter/X",
        "fa": "👉 یکی را کپی کنید، شخصی‌سازی کنید و در توییتر/X پست کنید",
        "ar": "👉 انسخ واحدة، خصصها وانشرها على تويتر/X",
    },
    "tweet_paste_url": {
        "en": "✅ *When done, paste your tweet URL below*\n(e.g. https://x.com/yourname/status/123...)",
        "fa": "✅ *وقتی تمام شد، لینک توییت خود را در زیر بگذارید*\n(مثلاً https://x.com/yourname/status/123...)",
        "ar": "✅ *عند الانتهاء، الصق رابط تغريدتك أدناه*\n(مثلاً https://x.com/yourname/status/123...)",
    },
    "tweet_what_to_do": {
        "en": "📝 *What to do:*",
        "fa": "📝 *چه کاری انجام دهید:*",
        "ar": "📝 *ما يجب فعله:*",
    },
    "comment_target_tweet": {
        "en": "🔗 *Tweet to comment on:*",
        "fa": "🔗 *توییتی که باید روی آن نظر بدهید:*",
        "ar": "🔗 *التغريدة للتعليق عليها:*",
    },
    "key_tweets_to_comment": {
        "en": "Key tweets to comment on",
        "fa": "توییت‌های کلیدی برای نظر دادن",
        "ar": "تغريدات رئيسية للتعليق عليها",
    },
    "comment_paste_reply_url": {
        "en": "✅ *When done, paste your reply/comment URL below*\n(e.g. https://x.com/yourname/status/123...)",
        "fa": "✅ *وقتی تمام شد، لینک پاسخ/نظر خود را در زیر بگذارید*\n(مثلاً https://x.com/yourname/status/123...)",
        "ar": "✅ *عند الانتهاء، الصق رابط ردك/تعليقك أدناه*\n(مثلاً https://x.com/yourname/status/123...)",
    },
    "task_paste_proof": {
        "en": "✅ *When done, paste the message link or send a screenshot*",
        "fa": "✅ *وقتی تمام شد، لینک پیام یا اسکرین‌شات بفرستید*",
        "ar": "✅ *عند الانتهاء، الصق رابط الرسالة أو أرسل لقطة شاشة*",
    },
    "task_share_bot_link": {
        "en": "👉 Share this link: https://t.me/peopleforpeacebot",
        "fa": "👉 این لینک را به اشتراک بگذارید: https://t.me/peopleforpeacebot",
        "ar": "👉 شارك هذا الرابط: https://t.me/peopleforpeacebot",
    },
    "task_send_username": {
        "en": "✅ *When done, send the username of the person you invited*",
        "fa": "✅ *وقتی تمام شد، نام کاربری شخصی که دعوت کردید را بفرستید*",
        "ar": "✅ *عند الانتهاء، أرسل اسم المستخدم للشخص الذي دعوته*",
    },
    "task_send_proof_generic": {
        "en": "✅ *When done, send your proof (text, link, or screenshot)*",
        "fa": "✅ *وقتی تمام شد، مدرک خود را بفرستید (متن، لینک، یا اسکرین‌شات)*",
        "ar": "✅ *عند الانتهاء، أرسل دليلك (نص، رابط، أو لقطة شاشة)*",
    },
    "cancel_hint": {
        "en": "Type /cancel to cancel.",
        "fa": "برای لغو /cancel را تایپ کنید.",
        "ar": "اكتب /cancel للإلغاء.",
    },

    # ── Proof Submission ──────────────────────────────────────────────
    "proof_review_title": {
        "en": "📝 *Proof Submission Review*",
        "fa": "📝 *بررسی ارسال مدرک*",
        "ar": "📝 *مراجعة تقديم الدليل*",
    },
    "proof_confirm": {
        "en": "Please confirm your submission:",
        "fa": "لطفاً ارسال خود را تأیید کنید:",
        "ar": "يرجى تأكيد تقديمك:",
    },
    "btn_confirm_submit": {
        "en": "✅ Confirm Submission",
        "fa": "✅ تأیید ارسال",
        "ar": "✅ تأكيد التقديم",
    },
    "btn_cancel": {
        "en": "❌ Cancel",
        "fa": "❌ لغو",
        "ar": "❌ إلغاء",
    },
    "proof_success": {
        "en": (
            "✅ *Proof Submitted Successfully!*\n\n"
            "*Task:* {task}\n"
            "*Status:* Pending Review\n"
            "*Points:* {points} (pending verification)\n\n"
            "Your proof has been submitted for review by the campaign manager.\n"
            "You'll be notified once it's verified and points are awarded."
        ),
        "fa": (
            "✅ *مدرک با موفقیت ارسال شد!*\n\n"
            "*وظیفه:* {task}\n"
            "*وضعیت:* در انتظار بررسی\n"
            "*امتیاز:* {points} (در انتظار تأیید)\n\n"
            "مدرک شما برای بررسی توسط مدیر کمپین ارسال شد.\n"
            "پس از تأیید و اعطای امتیاز به شما اطلاع داده می‌شود."
        ),
        "ar": (
            "✅ *تم تقديم الدليل بنجاح!*\n\n"
            "*المهمة:* {task}\n"
            "*الحالة:* قيد المراجعة\n"
            "*النقاط:* {points} (في انتظار التحقق)\n\n"
            "تم تقديم دليلك للمراجعة من قبل مدير الحملة.\n"
            "سيتم إخطارك بمجرد التحقق ومنح النقاط."
        ),
    },
    "proof_cancelled": {
        "en": "❌ Proof submission cancelled.\nUse `/mytasks` to view your tasks and submit proof later.",
        "fa": "❌ ارسال مدرک لغو شد.\nاز `/mytasks` برای مشاهده وظایف و ارسال مدرک بعداً استفاده کنید.",
        "ar": "❌ تم إلغاء تقديم الدليل.\nاستخدم `/mytasks` لعرض مهامك وتقديم الدليل لاحقاً.",
    },

    # ── Help ───────────────────────────────────────────────────────────
    "help_text": {
        "en": (
            "*People for Peace Campaign Manager - Help*\n\n"
            "*Available Commands:*\n"
            "/start - Start the bot and show welcome message\n"
            "/help - Show this help message\n"
            "/language - Change language\n"
            "/campaigns - List available campaigns\n"
            "/tasks - Show available tasks\n"
            "/mytasks - Show your assigned tasks\n"
            "/profile - Show your profile and points\n"
            "/leaderboard - Show top volunteers\n"
            "/storms - Show upcoming Twitter storms\n\n"
            "*How to Participate:*\n"
            "1. Browse campaigns with /campaigns\n"
            "2. Join a campaign\n"
            "3. Claim tasks with /tasks\n"
            "4. Complete tasks and submit proof\n"
            "5. Earn points and climb the leaderboard!\n\n"
            "Need more help? Contact your campaign manager."
        ),
        "fa": (
            "*مدیریت کمپین مردم برای صلح - راهنما*\n\n"
            "*دستورات موجود:*\n"
            "/start - شروع ربات و نمایش پیام خوش‌آمد\n"
            "/help - نمایش این راهنما\n"
            "/language - تغییر زبان\n"
            "/campaigns - لیست کمپین‌های موجود\n"
            "/tasks - نمایش وظایف موجود\n"
            "/mytasks - نمایش وظایف شما\n"
            "/profile - نمایش پروفایل و امتیازات\n"
            "/leaderboard - نمایش داوطلبان برتر\n"
            "/storms - نمایش طوفان‌های توییتری\n\n"
            "*نحوه مشارکت:*\n"
            "۱. کمپین‌ها را با /campaigns مرور کنید\n"
            "۲. به یک کمپین بپیوندید\n"
            "۳. وظایف را با /tasks انتخاب کنید\n"
            "۴. وظایف را انجام دهید و مدرک ارسال کنید\n"
            "۵. امتیاز کسب کنید و در جدول بالا بروید!\n\n"
            "نیاز به کمک بیشتر دارید؟ با مدیر کمپین تماس بگیرید."
        ),
        "ar": (
            "*مدير حملات الناس من أجل السلام - مساعدة*\n\n"
            "*الأوامر المتاحة:*\n"
            "/start - بدء البوت وعرض رسالة الترحيب\n"
            "/help - عرض رسالة المساعدة\n"
            "/language - تغيير اللغة\n"
            "/campaigns - عرض الحملات المتاحة\n"
            "/tasks - عرض المهام المتاحة\n"
            "/mytasks - عرض مهامك المعينة\n"
            "/profile - عرض ملفك الشخصي ونقاطك\n"
            "/leaderboard - عرض أفضل المتطوعين\n"
            "/storms - عرض عواصف تويتر القادمة\n\n"
            "*كيفية المشاركة:*\n"
            "١. تصفح الحملات مع /campaigns\n"
            "٢. انضم إلى حملة\n"
            "٣. طالب بالمهام مع /tasks\n"
            "٤. أكمل المهام وقدم دليلاً\n"
            "٥. اكسب نقاطاً وتسلق لوحة المتصدرين!\n\n"
            "تحتاج مزيداً من المساعدة؟ تواصل مع مدير حملتك."
        ),
    },

    # ── Errors ─────────────────────────────────────────────────────────
    "error_generic": {
        "en": "❌ An error occurred.\n\nOur team has been notified. Please try again later.",
        "fa": "❌ خطایی رخ داد.\n\nتیم ما مطلع شده است. لطفاً بعداً دوباره امتحان کنید.",
        "ar": "❌ حدث خطأ.\n\nتم إخطار فريقنا. يرجى المحاولة مرة أخرى لاحقاً.",
    },
    "error_need_join": {
        "en": "❌ You need to join this campaign first to claim its tasks.",
        "fa": "❌ برای انتخاب وظایف ابتدا باید عضو این کمپین شوید.",
        "ar": "❌ يجب عليك الانضمام إلى هذه الحملة أولاً للمطالبة بمهامها.",
    },
    "no_campaigns_joined": {
        "en": "📭 You haven't joined any campaigns yet.\nUse `/campaigns` to browse and join available campaigns.",
        "fa": "📭 هنوز عضو هیچ کمپینی نشده‌اید.\nاز `/campaigns` برای مرور و عضویت استفاده کنید.",
        "ar": "📭 لم تنضم إلى أي حملة بعد.\nاستخدم `/campaigns` لتصفح الحملات المتاحة والانضمام إليها.",
    },

    # ── Campaign Detail ────────────────────────────────────────────────
    "campaign_detail_volunteers": {
        "en": "👥 {current}/{target} volunteers joined",
        "fa": "👥 {current}/{target} داوطلب پیوسته‌اند",
        "ar": "👥 {current}/{target} متطوع انضموا",
    },
    "campaign_detail_tasks": {
        "en": "🎯 {count} tasks available",
        "fa": "🎯 {count} وظیفه موجود",
        "ar": "🎯 {count} مهمة متاحة",
    },
    "campaign_already_in": {
        "en": "✅ *You're in this campaign!*",
        "fa": "✅ *شما عضو این کمپین هستید!*",
        "ar": "✅ *أنت في هذه الحملة!*",
    },
    "campaign_tap_tasks": {
        "en": "Tap below to see your tasks and start making an impact.",
        "fa": "برای دیدن وظایف و شروع تأثیرگذاری، دکمه زیر را بزنید.",
        "ar": "اضغط أدناه لرؤية مهامك والبدء في إحداث تأثير.",
    },
    "campaign_ready_join": {
        "en": "Ready to make a difference? Join and start completing tasks.",
        "fa": "آماده‌اید تفاوت ایجاد کنید؟ عضو شوید و وظایف را شروع کنید.",
        "ar": "مستعد لإحداث فرق؟ انضم وابدأ بإكمال المهام.",
    },
    "btn_view_tasks_icon": {
        "en": "🎯 View Tasks",
        "fa": "🎯 مشاهده وظایف",
        "ar": "🎯 عرض المهام",
    },
    "btn_join_campaign": {
        "en": "✊ Join This Campaign",
        "fa": "✊ عضویت در این کمپین",
        "ar": "✊ انضم لهذه الحملة",
    },
    "btn_main_menu": {
        "en": "🏠 Main Menu",
        "fa": "🏠 منوی اصلی",
        "ar": "🏠 القائمة الرئيسية",
    },

    # ── Campaign Join ──────────────────────────────────────────────────
    "campaign_join_welcome": {
        "en": (
            "🎉 *You're in! Welcome to {name}*\n\n"
            "You've joined {count} other volunteers in this campaign.\n\n"
            "There are *{tasks} tasks* waiting for you — tweets to post, "
            "content to share, and voices to amplify.\n\n"
            "Tap *View Tasks* below to pick your first task and start earning points! 👇"
        ),
        "fa": (
            "🎉 *عضو شدید! به {name} خوش آمدید*\n\n"
            "شما به {count} داوطلب دیگر در این کمپین پیوستید.\n\n"
            "*{tasks} وظیفه* در انتظار شماست — توییت‌هایی برای ارسال، "
            "محتوا برای اشتراک‌گذاری و صداهایی برای تقویت.\n\n"
            "برای انتخاب اولین وظیفه و کسب امتیاز، *مشاهده وظایف* را بزنید! 👇"
        ),
        "ar": (
            "🎉 *انضممت! مرحباً في {name}*\n\n"
            "انضممت إلى {count} متطوع آخر في هذه الحملة.\n\n"
            "هناك *{tasks} مهمة* في انتظارك — تغريدات للنشر، "
            "محتوى للمشاركة، وأصوات لتضخيمها.\n\n"
            "اضغط *عرض المهام* أدناه لاختيار أول مهمة والبدء بكسب النقاط! 👇"
        ),
    },

    # ── Task Checklist View ────────────────────────────────────────────
    "checklist_title": {
        "en": "📋 *Your Tasks — {name}*",
        "fa": "📋 *وظایف شما — {name}*",
        "ar": "📋 *مهامك — {name}*",
    },
    "checklist_progress": {
        "en": "📊 {done}/{total} done · {points} pts earned",
        "fa": "📊 {done}/{total} انجام شده · {points} امتیاز کسب شده",
        "ar": "📊 {done}/{total} مكتمل · {points} نقطة مكتسبة",
    },
    "checklist_tap_start": {
        "en": "Tap a task to start 👇",
        "fa": "یک وظیفه را بزنید تا شروع کنید 👇",
        "ar": "اضغط على مهمة للبدء 👇",
    },

    # ── Community Pulse ────────────────────────────────────────────────
    "pulse_active_hour": {
        "en": "🫂 {count} activists active in the last hour",
        "fa": "🫂 {count} فعال در یک ساعت گذشته",
        "ar": "🫂 {count} ناشط نشط في الساعة الأخيرة",
    },
    "pulse_total_actions": {
        "en": "🔥 {count} total actions this campaign",
        "fa": "🔥 {count} اقدام کل در این کمپین",
        "ar": "🔥 {count} إجراء إجمالي في هذه الحملة",
    },
    "pulse_volunteers": {
        "en": "👥 {count} volunteers fighting together",
        "fa": "👥 {count} داوطلب در کنار هم مبارزه می‌کنند",
        "ar": "👥 {count} متطوع يقاتلون معاً",
    },
    "pulse_rank": {
        "en": "📊 You're in the Top {rank}%!",
        "fa": "📊 شما در {rank}% برتر هستید!",
        "ar": "📊 أنت في أفضل {rank}%!",
    },
    "pulse_actions_by": {
        "en": "🔥 {actions} total actions by {volunteers} volunteers",
        "fa": "🔥 {actions} اقدام توسط {volunteers} داوطلب",
        "ar": "🔥 {actions} إجراء من {volunteers} متطوع",
    },
    "pulse_active_short": {
        "en": "🫂 {count} active in the last hour",
        "fa": "🫂 {count} فعال در ساعت اخیر",
        "ar": "🫂 {count} نشط في الساعة الأخيرة",
    },

    # ── Task Guidance Flow ─────────────────────────────────────────────
    "task_started_title": {
        "en": "✅ *Task started!*",
        "fa": "✅ *وظیفه شروع شد!*",
        "ar": "✅ *بدأت المهمة!*",
    },
    "task_3_steps": {
        "en": "Complete this task in 3 easy steps:",
        "fa": "این وظیفه را در ۳ مرحله آسان انجام دهید:",
        "ar": "أكمل هذه المهمة في 3 خطوات سهلة:",
    },
    "tweet_step1": {
        "en": "*① Pick a tweet* below and tap *📲 Post This Tweet*",
        "fa": "*① یک توییت* از پایین انتخاب کنید و *📲 ارسال این توییت* را بزنید",
        "ar": "*① اختر تغريدة* أدناه واضغط *📲 انشر هذه التغريدة*",
    },
    "tweet_step2": {
        "en": "*② Twitter will open* with your tweet ready — just hit Post!",
        "fa": "*② توییتر باز می‌شود* با توییت آماده — فقط ارسال را بزنید!",
        "ar": "*② سيفتح تويتر* مع تغريدتك جاهزة — فقط اضغط نشر!",
    },
    "tweet_step3": {
        "en": "*③ Come back here* and paste your tweet URL",
        "fa": "*③ به اینجا برگردید* و لینک توییت خود را بگذارید",
        "ar": "*③ عد إلى هنا* والصق رابط تغريدتك",
    },
    "tweet_or_write_own": {
        "en": "✍️ Or write your own tweet using the campaign hashtags.",
        "fa": "✍️ یا توییت خود را با هشتگ‌های کمپین بنویسید.",
        "ar": "✍️ أو اكتب تغريدتك الخاصة باستخدام هاشتاغات الحملة.",
    },
    "tweet_paste_url_below": {
        "en": "When done, *paste your tweet URL below* 👇",
        "fa": "وقتی تمام شد، *لینک توییت را در زیر بگذارید* 👇",
        "ar": "عند الانتهاء، *الصق رابط تغريدتك أدناه* 👇",
    },
    "retweet_step1": {
        "en": "*① Tap the button* below to find {hashtags} tweets",
        "fa": "*① دکمه زیر را بزنید* تا توییت‌های {hashtags} را پیدا کنید",
        "ar": "*① اضغط الزر* أدناه للعثور على تغريدات {hashtags}",
    },
    "retweet_step2": {
        "en": "*② Retweet at least 3* tweets you agree with",
        "fa": "*② حداقل ۳ توییت* که با آن‌ها موافقید را ریتوییت کنید",
        "ar": "*② أعد تغريد 3 على الأقل* من التغريدات التي توافق عليها",
    },
    "retweet_step3": {
        "en": "*③ Come back here* and paste any tweet URL as proof",
        "fa": "*③ به اینجا برگردید* و لینک هر توییت را به عنوان مدرک بگذارید",
        "ar": "*③ عد إلى هنا* والصق أي رابط تغريدة كدليل",
    },
    "retweet_paste_proof": {
        "en": "When done, *paste a tweet URL below* 👇",
        "fa": "وقتی تمام شد، *لینک یک توییت را در زیر بگذارید* 👇",
        "ar": "عند الانتهاء، *الصق رابط تغريدة أدناه* 👇",
    },
    "btn_find_tweets": {
        "en": "🔍 Find {hashtags} Tweets",
        "fa": "🔍 یافتن توییت‌های {hashtags}",
        "ar": "🔍 ابحث عن تغريدات {hashtags}",
    },
    "comment_step1": {
        "en": "*① Pick a suggested reply* and tap the button",
        "fa": "*① یک پاسخ پیشنهادی* را انتخاب کنید و دکمه را بزنید",
        "ar": "*① اختر رداً مقترحاً* واضغط الزر",
    },
    "comment_step2": {
        "en": "*② Twitter opens with your reply ready* — just hit Post!",
        "fa": "*② توییتر با پاسخ آماده باز می‌شود* — فقط ارسال را بزنید!",
        "ar": "*② سيفتح تويتر مع ردك جاهزاً* — فقط اضغط نشر!",
    },
    "comment_step3": {
        "en": "*③ Come back here* and paste your reply URL",
        "fa": "*③ به اینجا برگردید* و لینک پاسخ خود را بگذارید",
        "ar": "*③ عد إلى هنا* والصق رابط ردك",
    },
    "comment_pick_tweet": {
        "en": "🎯 *Pick a tweet to reply to:*",
        "fa": "🎯 *یک توییت برای پاسخ دادن انتخاب کنید:*",
        "ar": "🎯 *اختر تغريدة للرد عليها:*",
    },
    "comment_or_write_own": {
        "en": "✍️ Or write your own reply with the hashtags!",
        "fa": "✍️ یا پاسخ خودتان را با هشتگ‌ها بنویسید!",
        "ar": "✍️ أو اكتب ردك الخاص مع الهاشتاغات!",
    },
    "comment_paste_reply": {
        "en": "When done, *paste your reply URL below* 👇",
        "fa": "وقتی تمام شد، *لینک پاسخ را در زیر بگذارید* 👇",
        "ar": "عند الانتهاء، *الصق رابط ردك أدناه* 👇",
    },
    "btn_reply_to": {
        "en": "💬 Reply to {handle}",
        "fa": "💬 پاسخ به {handle}",
        "ar": "💬 رد على {handle}",
    },
    "btn_reply_suggested": {
        "en": "💬 Reply with Suggested Comment",
        "fa": "💬 پاسخ با نظر پیشنهادی",
        "ar": "💬 رد بتعليق مقترح",
    },
    "share_send_proof": {
        "en": "When done, send proof (link or screenshot) below 👇",
        "fa": "وقتی تمام شد، مدرک (لینک یا اسکرین‌شات) را در زیر بفرستید 👇",
        "ar": "عند الانتهاء، أرسل الدليل (رابط أو لقطة شاشة) أدناه 👇",
    },
    "invite_share_link": {
        "en": "Share the bot link: https://t.me/peopleforpeacebot",
        "fa": "لینک ربات را به اشتراک بگذارید: https://t.me/peopleforpeacebot",
        "ar": "شارك رابط البوت: https://t.me/peopleforpeacebot",
    },
    "invite_send_username": {
        "en": "When done, send the username of who you invited 👇",
        "fa": "وقتی تمام شد، نام کاربری شخصی که دعوت کردید را بفرستید 👇",
        "ar": "عند الانتهاء، أرسل اسم المستخدم للشخص الذي دعوته 👇",
    },
    "generic_send_proof": {
        "en": "When done, send your proof below 👇",
        "fa": "وقتی تمام شد، مدرک خود را در زیر بفرستید 👇",
        "ar": "عند الانتهاء، أرسل دليلك أدناه 👇",
    },
    "btn_post_tweet": {
        "en": "📲 Post Tweet #{n}",
        "fa": "📲 ارسال توییت #{n}",
        "ar": "📲 انشر التغريدة #{n}",
    },

    # ── Proof Submission (updated) ─────────────────────────────────────
    "proof_submitted_short": {
        "en": "✅ *Proof Submitted!* +{points} pts",
        "fa": "✅ *مدرک ارسال شد!* +{points} امتیاز",
        "ar": "✅ *تم تقديم الدليل!* +{points} نقطة",
    },
    "proof_under_review": {
        "en": "Your proof is being reviewed — you'll be notified once verified.",
        "fa": "مدرک شما در حال بررسی است — پس از تأیید به شما اطلاع داده می‌شود.",
        "ar": "يتم مراجعة دليلك — سيتم إخطارك بمجرد التحقق.",
    },
    "proof_keep_going": {
        "en": "Ready to keep going? 👇",
        "fa": "آماده ادامه هستید? 👇",
        "ar": "مستعد للاستمرار؟ 👇",
    },
    "btn_do_another": {
        "en": "🎯 Do Another Task",
        "fa": "🎯 انجام وظیفه دیگر",
        "ar": "🎯 قم بمهمة أخرى",
    },
    "btn_back_tasks": {
        "en": "↩️ Back to Tasks",
        "fa": "↩️ بازگشت به وظایف",
        "ar": "↩️ العودة إلى المهام",
    },

    # ── Task Detail (preview) ──────────────────────────────────────────
    "task_spots_remaining": {
        "en": "📊 {n} spots remaining",
        "fa": "📊 {n} جای باقیمانده",
        "ar": "📊 {n} مكان متبقي",
    },
    "task_tweet_desc": {
        "en": "You'll pick a ready-made tweet and post it on Twitter — takes about 1 minute!",
        "fa": "شما یک توییت آماده انتخاب می‌کنید و در توییتر ارسال می‌کنید — حدود ۱ دقیقه وقت می‌گیرد!",
        "ar": "ستختار تغريدة جاهزة وتنشرها على تويتر — تستغرق حوالي دقيقة واحدة!",
    },
    "task_retweet_desc": {
        "en": "You'll retweet key campaign tweets to amplify the message.",
        "fa": "توییت‌های کلیدی کمپین را ریتوییت می‌کنید تا پیام تقویت شود.",
        "ar": "ستعيد تغريد التغريدات الرئيسية للحملة لتضخيم الرسالة.",
    },
    "task_comment_desc": {
        "en": "You'll reply to key tweets to add your voice to the conversation.",
        "fa": "به توییت‌های کلیدی پاسخ می‌دهید تا صدای خود را به گفتگو اضافه کنید.",
        "ar": "سترد على التغريدات الرئيسية لإضافة صوتك إلى المحادثة.",
    },
    "btn_start_action": {
        "en": "🚀 Let's Go!",
        "fa": "🚀 بزن بریم!",
        "ar": "🚀 هيا بنا!",
    },

    # ── Invite Link Feature ──────────────────────────────────
    "btn_invite_friends": {
        "en": "📨 Invite Friends",
        "fa": "📨 دعوت دوستان",
        "ar": "📨 دعوة الأصدقاء",
    },
    "btn_share_link": {
        "en": "📤 Share via Telegram",
        "fa": "📤 اشتراک‌گذاری در تلگرام",
        "ar": "📤 مشاركة عبر تيليجرام",
    },

    # ── My Campaigns (simplified flow) ────────────────────────
    "my_campaigns_title": {
        "en": "✊ *Your Campaigns*",
        "fa": "✊ *کمپین‌های شما*",
        "ar": "✊ *حملاتك*",
    },
    "my_campaigns_tap": {
        "en": "Tap a campaign to see its tasks 👇",
        "fa": "روی یک کمپین بزنید تا وظایفش را ببینید 👇",
        "ar": "اضغط على حملة لرؤية مهامها 👇",
    },
    "campaigns_tasks_label": {
        "en": "tasks",
        "fa": "وظیفه",
        "ar": "مهام",
    },

    # ── New Task Types (Petition & Mass Email) ────────────────
    "task_petition_title": {
        "en": "✍️ Sign the Petition",
        "fa": "✍️ امضای طومار",
        "ar": "✍️ وقّع العريضة",
    },
    "task_petition_step1": {
        "en": "Tap the link below to open the petition page:",
        "fa": "روی لینک زیر بزنید تا صفحه طومار باز شود:",
        "ar": "اضغط على الرابط أدناه لفتح صفحة العريضة:",
    },
    "task_petition_step2": {
        "en": "Sign the petition with your name and email.",
        "fa": "طومار را با نام و ایمیل خود امضا کنید.",
        "ar": "وقّع العريضة باسمك وبريدك الإلكتروني.",
    },
    "task_petition_step3": {
        "en": "Come back here and send a screenshot as proof ✅",
        "fa": "برگردید اینجا و اسکرین‌شات را به عنوان مدرک بفرستید ✅",
        "ar": "عُد هنا وأرسل لقطة شاشة كدليل ✅",
    },
    "btn_open_petition": {
        "en": "✍️ Open Petition",
        "fa": "✍️ باز کردن طومار",
        "ar": "✍️ فتح العريضة",
    },
    "task_mass_email_title": {
        "en": "📧 Send Mass Email",
        "fa": "📧 ارسال ایمیل گروهی",
        "ar": "📧 إرسال بريد جماعي",
    },
    "task_mass_email_step1": {
        "en": "Copy the email template below and send it to the listed organizations.",
        "fa": "متن ایمیل زیر را کپی کنید و به سازمان‌های لیست شده بفرستید.",
        "ar": "انسخ نموذج البريد أدناه وأرسله إلى المنظمات المدرجة.",
    },
    "task_mass_email_step2": {
        "en": "Come back here and confirm you've sent the emails ✅",
        "fa": "برگردید اینجا و تأیید کنید که ایمیل‌ها را فرستاده‌اید ✅",
        "ar": "عُد هنا وأكّد أنك أرسلت الرسائل ✅",
    },
    "btn_copy_email": {
        "en": "📋 Copy Email Template",
        "fa": "📋 کپی متن ایمیل",
        "ar": "📋 نسخ نموذج البريد",
    },

    "invite_message": {
        "en": (
            "📨 *Invite Friends to {name}*\n\n"
            "Share this link with friends and family to join the campaign:\n\n"
            "`{link}`\n\n"
            "When someone joins through your link, you earn *+10 bonus points!* 🎁\n\n"
            "Tap the button below to share directly 👇"
        ),
        "fa": (
            "📨 *دعوت دوستان به {name}*\n\n"
            "این لینک را با دوستان و خانواده به اشتراک بگذارید:\n\n"
            "`{link}`\n\n"
            "وقتی کسی از طریق لینک شما بپیوندد، *+۱۰ امتیاز ویژه* دریافت می‌کنید! 🎁\n\n"
            "برای اشتراک‌گذاری مستقیم دکمه زیر را بزنید 👇"
        ),
        "ar": (
            "📨 *دعوة الأصدقاء إلى {name}*\n\n"
            "شارك هذا الرابط مع أصدقائك وعائلتك:\n\n"
            "`{link}`\n\n"
            "عندما ينضم شخص عبر رابطك، تحصل على *+١٠ نقاط إضافية!* 🎁\n\n"
            "اضغط الزر أدناه للمشاركة مباشرة 👇"
        ),
    },
    "invite_share_text": {
        "en": "Join me in the \"{name}\" campaign for peace! ✌️",
        "fa": "به کمپین «{name}» برای صلح بپیوندید! ✌️",
        "ar": "انضم إليّ في حملة «{name}» من أجل السلام! ✌️",
    },
    "referral_credited": {
        "en": "🎁 *+10 pts!* {name} just joined *{campaign}* through your invite link!",
        "fa": "🎁 *+۱۰ امتیاز!* {name} از طریق لینک دعوت شما به *{campaign}* پیوست!",
        "ar": "🎁 *+١٠ نقاط!* {name} انضم إلى *{campaign}* عبر رابط دعوتك!",
    },
}


def t(key: str, lang: str = 'en') -> str:
    """Get translated string by key and language code."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get('en', key))


def get_main_menu_inline(lang: str = 'en'):
    """Get the simplified main menu as InlineKeyboardMarkup.

    Layout (4 buttons):
      ✊ My Campaigns
      📨 Invite Friends
      🌍 Language  |  ℹ️ Help
    """
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [
            InlineKeyboardButton(t('btn_my_campaigns', lang), callback_data='menu_campaigns'),
        ],
        [
            InlineKeyboardButton(t('btn_invite_friends', lang), callback_data='menu_invite'),
        ],
        [
            InlineKeyboardButton(t('btn_language', lang), callback_data='menu_language'),
            InlineKeyboardButton(t('btn_help', lang), callback_data='menu_help'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_menu_inline(lang: str = 'en'):
    """Get a single 'Back to Menu' inline button."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    label = {'en': '🏠 Main Menu', 'fa': '🏠 منوی اصلی', 'ar': '🏠 القائمة الرئيسية'}
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label.get(lang, label['en']), callback_data='menu_main')]
    ])


def get_keyboard_buttons(lang: str = 'en') -> list[list[str]]:
    """Get the main ReplyKeyboard buttons in the given language."""
    return [
        [t('btn_my_campaigns', lang)],
        [t('btn_invite_friends', lang)],
        [t('btn_language', lang), t('btn_help', lang)],
    ]


def get_button_routes(lang: str = 'en') -> dict[str, str]:
    """Get button text → route mapping for the given language."""
    return {
        t('btn_campaigns', lang): '_route_campaigns',
        t('btn_my_campaigns', lang): '_route_campaigns',
        t('btn_tasks', lang): '_route_tasks',
        t('btn_progress', lang): '_route_profile',
        t('btn_leaderboard', lang): '_route_leaderboard',
        t('btn_help', lang): '_route_help',
        t('btn_profile', lang): '_route_profile',
        t('btn_language', lang): '_route_language',
        t('btn_invite_friends', lang): '_route_invite',
    }


# All possible button texts across all languages (for routing)
ALL_BUTTON_ROUTES: dict[str, str] = {}
for _lang in ('en', 'fa', 'ar'):
    ALL_BUTTON_ROUTES.update(get_button_routes(_lang))
