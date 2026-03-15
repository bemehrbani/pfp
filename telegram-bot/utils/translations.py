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
            "🕊️ *People for Peace*\n\n"
            "We're a volunteer network taking digital action for justice and peace.\n\n"
            "🤲 Every small action matters — a tweet, a signature, a share.\n\n"
            "Let's get started 👇"
        ),
        "fa": (
            "🕊️ *مردم برای صلح*\n\n"
            "ما یک شبکه داوطلب هستیم که برای عدالت و صلح اقدام دیجیتال انجام می‌دیم.\n\n"
            "🤲 هر اقدام کوچک مهمه — یک توییت، یک امضا، یک اشتراک‌گذاری.\n\n"
            "بزن بریم 👇"
        ),
        "ar": (
            "🕊️ *الناس من أجل السلام*\n\n"
            "نحن شبكة متطوعين نتخذ إجراءات رقمية من أجل العدالة والسلام.\n\n"
            "🤲 كل فعل صغير مهم — تغريدة، توقيع، مشاركة.\n\n"
            "لنبدأ 👇"
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
    "dashboard_not_authorized": {
        "en": "🔒 Dashboard access is for campaign managers and admins only.\n\nContact an admin if you need access.",
        "fa": "🔒 دسترسی به داشبورد فقط برای مدیران کمپین و ادمین‌ها است.\n\nاگر نیاز به دسترسی دارید با ادمین تماس بگیرید.",
        "ar": "🔒 الوصول إلى لوحة التحكم مخصص لمديري الحملات والمسؤولين فقط.\n\nتواصل مع المسؤول إذا كنت بحاجة إلى وصول.",
    },
    "dashboard_otp_sent": {
        "en": "🔐 *Dashboard Login Code*\n\n"
              "Your one-time code: `{code}`\n\n"
              "👤 Username: `{username}`\n"
              "⏱ Expires in 5 minutes\n\n"
              "Go to [peopleforpeace.live/dashboard](https://peopleforpeace.live/dashboard) and enter your username and this code to log in.",
        "fa": "🔐 *کد ورود به داشبورد*\n\n"
              "کد یک‌بار مصرف شما: `{code}`\n\n"
              "👤 نام کاربری: `{username}`\n"
              "⏱ انقضا در ۵ دقیقه\n\n"
              "به [peopleforpeace.live/dashboard](https://peopleforpeace.live/dashboard) بروید و نام کاربری و کد را وارد کنید.",
        "ar": "🔐 *رمز الدخول إلى لوحة التحكم*\n\n"
              "رمزك لمرة واحدة: `{code}`\n\n"
              "👤 اسم المستخدم: `{username}`\n"
              "⏱ ينتهي في 5 دقائق\n\n"
              "اذهب إلى [peopleforpeace.live/dashboard](https://peopleforpeace.live/dashboard) وأدخل اسم المستخدم والرمز لتسجيل الدخول.",
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
            "📅 *What happened:*\n"
            "On Feb 28, 2026, a school in Minab, Iran was bombed.\n"
            "168 children were killed.\n\n"
            "📋 *What we're doing:*\n"
            "We've identified names and photos of 168 children, "
            "built an online memorial, collected investigative reports, "
            "and launched an international petition.\n\n"
            "🤲 *How you help:*\n"
            "Complete simple tasks below — tweet a child's story, "
            "sign a petition, or amplify reports. Each takes ~2 min.\n\n"
            "👥 {members} volunteers · 🎯 {tasks} tasks\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕯 [Memorial](https://peopleforpeace.live/memorial.html)\n"
            "📄 [Evidence](https://peopleforpeace.live/evidence.html)\n"
            "📢 @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "⭐ Tasks are sorted by easiest first — start from the top! 👇"
        ),
        "fa": (
            "🎉 *شما به {name} پیوستید!*\n\n"
            "📅 *چه اتفاقی افتاد:*\n"
            "۹ اسفند ۱۴۰۴ — مدرسه‌ای در میناب بمباران شد.\n"
            "۱۶۸ کودک جان باختند.\n\n"
            "📋 *ما چیکار کردیم:*\n"
            "اسم و عکس ۱۶۸ کودک رو شناسایی کردیم، "
            "یادبود آنلاین ساختیم، گزارش‌های تحقیقی جمع کردیم "
            "و طومار بین‌المللی راه انداختیم.\n\n"
            "🤲 *شما چطور کمک می‌کنید:*\n"
            "وظایف ساده زیر رو انجام بدید — داستان یک کودک رو توییت کنید، "
            "طومار امضا کنید، یا گزارش‌ها رو تقویت کنید. هرکدوم ~۲ دقیقه.\n\n"
            "👥 {members} داوطلب · 🎯 {tasks} وظیفه\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕯 [یادبود](https://peopleforpeace.live/memorial.html)\n"
            "📄 [شواهد](https://peopleforpeace.live/evidence.html)\n"
            "📢 @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "⭐ وظایف از آسان‌ترین مرتب شدن — از بالا شروع کنید! 👇"
        ),
        "ar": (
            "🎉 *لقد انضممت إلى {name}!*\n\n"
            "📅 *ماذا حدث:*\n"
            "في ٢٨ فبراير ٢٠٢٦، قُصفت مدرسة في ميناب، إيران.\n"
            "قُتل ١٦٨ طفلاً.\n\n"
            "📋 *ماذا نفعل:*\n"
            "حددنا أسماء وصور ١٦٨ طفل، "
            "أنشأنا نصباً تذكارياً رقمياً، جمعنا تقارير تحقيقية، "
            "وأطلقنا عريضة دولية.\n\n"
            "🤲 *كيف تساعد:*\n"
            "أكمل المهام البسيطة أدناه — غرّد بقصة طفل، "
            "وقّع عريضة، أو ضخّم التقارير. كل مهمة ~دقيقتان.\n\n"
            "👥 {members} متطوع · 🎯 {tasks} مهمة\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕯 [التذكار](https://peopleforpeace.live/memorial.html)\n"
            "📄 [أدلة](https://peopleforpeace.live/evidence.html)\n"
            "📢 @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "اضغط على مهمة للبدء! 👇"
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
            "You'll be notified once it's verified and points are awarded.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕊️ People for Peace · peopleforpeace.live"
        ),
        "fa": (
            "✅ *مدرک با موفقیت ارسال شد!*\n\n"
            "*وظیفه:* {task}\n"
            "*وضعیت:* در انتظار بررسی\n"
            "*امتیاز:* {points} (در انتظار تأیید)\n\n"
            "مدرک شما برای بررسی توسط مدیر کمپین ارسال شد.\n"
            "پس از تأیید و اعطای امتیاز به شما اطلاع داده می‌شود.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕊️ مردم برای صلح · peopleforpeace.live"
        ),
        "ar": (
            "✅ *تم تقديم الدليل بنجاح!*\n\n"
            "*المهمة:* {task}\n"
            "*الحالة:* قيد المراجعة\n"
            "*النقاط:* {points} (في انتظار التحقق)\n\n"
            "تم تقديم دليلك للمراجعة من قبل مدير الحملة.\n"
            "سيتم إخطارك بمجرد التحقق ومنح النقاط.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🕊️ الناس من أجل السلام · peopleforpeace.live"
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
            "/profile - Show your profile\n"
            "/storms - Show upcoming Twitter storms\n\n"
            "*How to Participate:*\n"
            "1. Browse campaigns with /campaigns\n"
            "2. Join a campaign\n"
            "3. Claim tasks with /tasks\n"
            "4. Complete tasks and submit proof\n"
            "5. Complete tasks and make an impact!\n\n"
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
            "/profile - نمایش پروفایل\n"
            "/storms - نمایش طوفان‌های توییتری\n\n"
            "*نحوه مشارکت:*\n"
            "۱. کمپین‌ها را با /campaigns مرور کنید\n"
            "۲. به یک کمپین بپیوندید\n"
            "۳. وظایف را با /tasks انتخاب کنید\n"
            "۴. وظایف را انجام دهید و مدرک ارسال کنید\n"
            "۵. وظایف را انجام دهید و تأثیرگذار باشید!\n\n"
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
            "/profile - عرض ملفك الشخصي\n"
            "/storms - عرض عواصف تويتر القادمة\n\n"
            "*كيفية المشاركة:*\n"
            "١. تصفح الحملات مع /campaigns\n"
            "٢. انضم إلى حملة\n"
            "٣. طالب بالمهام مع /tasks\n"
            "٤. أكمل المهام وقدم دليلاً\n"
            "٥. أكمل المهام وأحدث تأثيراً!\n\n"
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
        "en": "👥 {current} volunteers joined",
        "fa": "👥 {current} داوطلب پیوسته‌اند",
        "ar": "👥 {current} متطوع انضموا",
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
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *Resources:*\n"
            "🕯 [Memorial](https://peopleforpeace.live)\n"
            "📄 [Evidence & Facts](https://peopleforpeace.live/evidence.html)\n"
            "📊 [Verified Data](https://peopleforpeace.live/data.html)\n"
            "📢 Follow: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "Tap *View Tasks* below to pick your first task! 👇"
        ),
        "fa": (
            "🎉 *عضو شدید! به {name} خوش آمدید*\n\n"
            "شما به {count} داوطلب دیگر در این کمپین پیوستید.\n\n"
            "*{tasks} وظیفه* در انتظار شماست — توییت‌هایی برای ارسال، "
            "محتوا برای اشتراک‌گذاری و صداهایی برای تقویت.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *منابع:*\n"
            "🕯 [صفحه یادبود](https://peopleforpeace.live)\n"
            "📄 [شواهد و حقایق](https://peopleforpeace.live/evidence.html)\n"
            "📊 [داده‌های تأییدشده](https://peopleforpeace.live/data.html)\n"
            "📢 دنبال کنید: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "برای انتخاب اولین وظیفه، *مشاهده وظایف* را بزنید! 👇"
        ),
        "ar": (
            "🎉 *انضممت! مرحباً في {name}*\n\n"
            "انضممت إلى {count} متطوع آخر في هذه الحملة.\n\n"
            "هناك *{tasks} مهمة* في انتظارك — تغريدات للنشر، "
            "محتوى للمشاركة، وأصوات لتضخيمها.\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *الموارد:*\n"
            "🕯 [صفحة التذكار](https://peopleforpeace.live)\n"
            "📄 [أدلة وحقائق](https://peopleforpeace.live/evidence.html)\n"
            "📊 [بيانات موثقة](https://peopleforpeace.live/data.html)\n"
            "📢 تابعنا: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "اضغط *عرض المهام* أدناه لاختيار أول مهمة! 👇"
        ),
    },

    # ── Task Checklist View ────────────────────────────────────────────
    "checklist_title": {
        "en": (
            "📋 *Your Tasks — {name}*\n\n"
            "🕯 168 children. One school. We demand justice.\n"
            "Every action here amplifies their story."
        ),
        "fa": (
            "📋 *وظایف شما — {name}*\n\n"
            "🕯 ۱۶۸ کودک. یک مدرسه. ما خواهان عدالتیم.\n"
            "هر اقدام شما صدای آن‌ها را بلندتر می‌کند."
        ),
        "ar": (
            "📋 *مهامك — {name}*\n\n"
            "🕯 ١٦٨ طفلاً. مدرسة واحدة. نطالب بالعدالة.\n"
            "كل عمل هنا يضخّم قصتهم."
        ),
    },
    "checklist_progress": {
        "en": "📊 {done}/{total} done · {points} pts earned",
        "fa": "📊 {done}/{total} انجام شده · {points} امتیاز کسب شده",
        "ar": "📊 {done}/{total} مكتمل · {points} نقطة مكتسبة",
    },
    "checklist_tap_start": {
        "en": "Tap a task to get started 👇",
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
    # ── Dual-Path Amplify ──────────────────────────────────────────────
    "amplify_choose_platform": {
        "en": "📣 *Choose how to amplify:*",
        "fa": "📣 *روش تقویت را انتخاب کنید:*",
        "ar": "📣 *اختر طريقة التضخيم:*",
    },
    "amplify_twitter_path": {
        "en": "🐦 *Option A — Twitter:*",
        "fa": "🐦 *گزینه الف — توییتر:*",
        "ar": "🐦 *الخيار أ — تويتر:*",
    },
    "amplify_telegram_path": {
        "en": "📢 *Option B — Forward on Telegram:*",
        "fa": "📢 *گزینه ب — فوروارد در تلگرام:*",
        "ar": "📢 *الخيار ب — إعادة توجيه عبر تيليجرام:*",
    },
    "amplify_tg_step1": {
        "en": "*① Tap 'Get Message'* below to receive a ready-to-forward message",
        "fa": "*① دکمه 'دریافت پیام'* رو بزنید تا یک پیام آماده برای فوروارد دریافت کنید",
        "ar": "*① اضغط 'استلام رسالة'* لتلقي رسالة جاهزة للتوجيه",
    },
    "amplify_tg_step2": {
        "en": "*② Forward it* to 3+ groups or contacts",
        "fa": "*② فوروارد کنید* به ۳ گروه یا مخاطب یا بیشتر",
        "ar": "*② أعد توجيهها* إلى ٣+ مجموعات أو جهات اتصال",
    },
    "amplify_tg_step3": {
        "en": "*③ Come back* and send a screenshot or type 'done'",
        "fa": "*③ برگردید* و اسکرین‌شات بفرستید یا بنویسید 'done'",
        "ar": "*③ عد* وأرسل لقطة شاشة أو اكتب 'done'",
    },
    "btn_get_forward_msg": {
        "en": "📢 Get Forwardable Message",
        "fa": "📢 دریافت پیام آماده فوروارد",
        "ar": "📢 استلام رسالة جاهزة",
    },
    "amplify_proof_hint": {
        "en": "When done, *paste a tweet URL* or *send a screenshot* of your forwards 👇",
        "fa": "وقتی تمام شد، *لینک توییت* یا *اسکرین‌شات فوروارد* رو بفرستید 👇",
        "ar": "عند الانتهاء، *الصق رابط تغريدة* أو *أرسل لقطة شاشة* للتوجيهات 👇",
    },
    "amplify_forward_instruction": {
        "en": "⬆️ Forward the message above to 3+ Telegram groups or contacts, then send a screenshot here as proof.",
        "fa": "⬆️ پیام بالا رو به ۳ گروه یا مخاطب فوروارد کنید، بعد اسکرین‌شات رو اینجا بفرستید.",
        "ar": "⬆️ أعد توجيه الرسالة أعلاه إلى ٣+ مجموعات أو جهات اتصال، ثم أرسل لقطة شاشة كدليل.",
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

    # ── Proof Submission (auto-verified) ─────────────────────────────────
    "proof_submitted_short": {
        "en": "✅ *Task Completed!*",
        "fa": "✅ *وظیفه انجام شد!*",
        "ar": "✅ *تم إنجاز المهمة!*",
    },
    "proof_auto_completed": {
        "en": "Thank you for your action — every step makes a difference 🕊",
        "fa": "ممنون از اقدام شما — هر قدمی تأثیرگذار است 🕊",
        "ar": "شكراً لتحركك — كل خطوة تُحدث فرقاً 🕊",
    },
    "proof_keep_going": {
        "en": "Ready to keep going? 👇",
        "fa": "آماده ادامه هستید? 👇",
        "ar": "مستعد للاستمرار؟ 👇",
    },

    # ── Twitter Like ──────────────────────────────────────────────────
    "like_instructions": {
        "en": "❤️ *Like these tweets to boost their reach!*\n\nTap each button to open the tweet, then like it.",
        "fa": "❤️ *این توییت‌ها را لایک کنید تا بازدیدشان بالا برود!*\n\nروی هر دکمه بزنید و توییت را لایک کنید.",
        "ar": "❤️ *أعجب بهذه التغريدات لزيادة وصولها!*\n\nاضغط كل زر لفتح التغريدة ثم أعجب بها.",
    },
    "btn_like_tweet": {
        "en": "❤️ Like {handle}",
        "fa": "❤️ لایک {handle}",
        "ar": "❤️ إعجاب {handle}",
    },
    "like_send_done": {
        "en": "👉 When done, send *done* to confirm.",
        "fa": "👉 بعد از اتمام، بنویسید *done* برای تأیید.",
        "ar": "👉 عند الانتهاء، أرسل *done* للتأكيد.",
    },

    # ── Content Creation ──────────────────────────────────────────────
    "content_creation_instructions": {
        "en": (
            "🎨 *Create Art for Peace*\n\n"
            "168 children were killed in the Minab school attack. "
            "Your art can tell their story to the world.\n\n"
            "*What you can create:*\n"
            "🖌 Illustration or digital art\n"
            "📝 Poem or spoken word\n"
            "🎬 Short video or animation\n"
            "📷 Photo collage or photo art\n"
            "🎵 Music or sound piece\n\n"
            "*Steps:*\n"
            "1️⃣ Browse the Memorial for inspiration\n"
            "2️⃣ Create your piece (any language, any medium)\n"
            "3️⃣ Share on your social media with #JusticeForMinab\n"
            "4️⃣ Send it here as proof (photo, video, or link)"
        ),
        "fa": (
            "🎨 *هنر برای صلح*\n\n"
            "۱۶۸ کودک در حمله به مدرسه میناب کشته شدند. "
            "هنر شما می‌تواند داستان آن‌ها را به جهان بگوید.\n\n"
            "*چه چیزی می‌توانید بسازید:*\n"
            "🖌 تصویرسازی یا هنر دیجیتال\n"
            "📝 شعر یا متن ادبی\n"
            "🎬 ویدیو یا انیمیشن کوتاه\n"
            "📷 کلاژ عکس یا فتوآرت\n"
            "🎵 موسیقی یا قطعه صوتی\n\n"
            "*مراحل:*\n"
            "1️⃣ یادبود را برای الهام مرور کنید\n"
            "2️⃣ اثر خود را بسازید (هر زبان، هر فرمت)\n"
            "3️⃣ در شبکه‌های اجتماعی با #JusticeForMinab به اشتراک بگذارید\n"
            "4️⃣ به عنوان مدرک اینجا ارسال کنید (عکس، ویدیو یا لینک)"
        ),
        "ar": (
            "🎨 *فن من أجل السلام*\n\n"
            "قُتل ١٦٨ طفلاً في هجوم مدرسة ميناب. "
            "فنك يمكن أن يروي قصتهم للعالم.\n\n"
            "*ما يمكنك إنشاؤه:*\n"
            "🖌 رسم توضيحي أو فن رقمي\n"
            "📝 شعر أو كلمة مسموعة\n"
            "🎬 فيديو قصير أو رسوم متحركة\n"
            "📷 كولاج صور أو فن فوتوغرافي\n"
            "🎵 موسيقى أو قطعة صوتية\n\n"
            "*الخطوات:*\n"
            "1️⃣ تصفح النصب التذكاري للإلهام\n"
            "2️⃣ أنشئ عملك (أي لغة، أي وسيلة)\n"
            "3️⃣ شارك على وسائل التواصل مع #JusticeForMinab\n"
            "4️⃣ أرسله هنا كدليل (صورة أو فيديو أو رابط)"
        ),
    },
    "btn_content_library": {
        "en": "🕯 Memorial — Minab Children",
        "fa": "🕯 یادبود — کودکان میناب",
        "ar": "🕯 النصب التذكاري — أطفال ميناب",
    },
    "btn_evidence_reports": {
        "en": "📰 Evidence & Reports",
        "fa": "📰 مدارک و گزارش‌ها",
        "ar": "📰 الأدلة والتقارير",
    },
    "content_creation_proof": {
        "en": "📤 Send your art below — photo, video, or link to your post 👇",
        "fa": "📤 هنر خود را ارسال کنید — عکس، ویدیو، یا لینک 👇",
        "ar": "📤 أرسل فنك أدناه — صورة أو فيديو أو رابط 👇",
    },
    "content_child_inspiration": {
        "en": "🕯 *{name}* — one of the 168 children of Minab. Let their memory inspire your art.",
        "fa": "🕯 *{name}* — یکی از ۱۶۸ کودک میناب. بگذارید یاد آن‌ها الهام‌بخش هنر شما باشد.",
        "ar": "🕯 *{name}* — أحد أطفال ميناب الـ ١٦٨. دع ذكراهم تلهم فنك.",
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
    "btn_back_to_tasks": {
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
    "task_instructions_title": {
        "en": "Instructions",
        "fa": "دستورالعمل",
        "ar": "التعليمات",
    },
    "task_duration": {
        "en": "Duration",
        "fa": "مدت زمان",
        "ar": "المدة",
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
            "_{description}_\n\n"
            "Share this link with friends and family to join the campaign:\n\n"
            "`{link}`\n\n"
            "Every person who joins makes a difference ✊\n\n"
            "Tap the button below to share directly 👇"
        ),
        "fa": (
            "📨 *دعوت دوستان به {name}*\n\n"
            "_{description}_\n\n"
            "این لینک را با دوستان و خانواده به اشتراک بگذارید:\n\n"
            "`{link}`\n\n"
            "هر نفری که بپیوندد، تأثیرگذار است ✊\n\n"
            "برای اشتراک‌گذاری مستقیم دکمه زیر را بزنید 👇"
        ),
        "ar": (
            "📨 *دعوة الأصدقاء إلى {name}*\n\n"
            "_{description}_\n\n"
            "شارك هذا الرابط مع أصدقائك وعائلتك:\n\n"
            "`{link}`\n\n"
            "كل شخص ينضم يُحدث فرقاً ✊\n\n"
            "اضغط الزر أدناه للمشاركة مباشرة 👇"
        ),
    },
    "invite_share_text": {
        "en": "Join me in the \"{name}\" campaign for peace! ✌️",
        "fa": "به کمپین «{name}» برای صلح بپیوندید! ✌️",
        "ar": "انضم إليّ في حملة «{name}» من أجل السلام! ✌️",
    },
    "referral_credited": {
        "en": "🎁 *Great!* {name} just joined *{campaign}* through your invite link! Welcome them! 🤝",
        "fa": "🎁 *عالی!* {name} از طریق لینک دعوت شما به *{campaign}* پیوست! خوش‌آمدشان بگویید! 🤝",
        "ar": "🎁 *رائع!* {name} انضم إلى *{campaign}* عبر رابط دعوتك! رحّبوا بهم! 🤝",
    },

    # ── Invite Flow: Language & Style Picker ──
    "invite_pick_language": {
        "en": "📨 *Invite Friends*\n\nChoose the language for your invite message:",
        "fa": "📨 *دعوت دوستان*\n\nزبان پیام دعوت خود را انتخاب کنید:",
        "ar": "📨 *دعوة الأصدقاء*\n\nاختر لغة رسالة الدعوة:",
    },
    "invite_pick_style": {
        "en": (
            "📨 *Choose a message to share:*\n\n"
            "🕯 *Memorial* — Children of Minab\n"
            "_Sends a photo with emotional message_\n\n"
            "🎬 *Video* — 100 Faces of Peace\n"
            "_Sends the lyric video in chosen language_\n\n"
            "✊ *Campaign* — Join the movement\n"
            "_Sends a text invite with action CTA_"
        ),
        "fa": (
            "📨 *یک پیام برای اشتراک‌گذاری انتخاب کنید:*\n\n"
            "🕯 *یادبود* — کودکان میناب\n"
            "_عکس با پیام احساسی ارسال می‌شود_\n\n"
            "🎬 *ویدیو* — صد چهره‌ی صلح\n"
            "_ویدیوی موزیک به زبان انتخابی ارسال می‌شود_\n\n"
            "✊ *کمپین* — به جنبش بپیوندید\n"
            "_پیام متنی با دعوت به اقدام ارسال می‌شود_"
        ),
        "ar": (
            "📨 *اختر رسالة للمشاركة:*\n\n"
            "🕯 *النصب التذكاري* — أطفال ميناب\n"
            "_يُرسل صورة مع رسالة مؤثرة_\n\n"
            "🎬 *فيديو* — مئة وجه للسلام\n"
            "_يُرسل الفيديو الموسيقي باللغة المختارة_\n\n"
            "✊ *الحملة* — انضم للحركة\n"
            "_يُرسل دعوة نصية مع دعوة للتحرك_"
        ),
    },
    "invite_memorial_caption": {
        "en": (
            "🕯 168 children were killed in the Minab school attack.\n\n"
            "Their names have been identified. Their photos collected.\n"
            "We're keeping their case alive.\n\n"
            "🤲 You can help — just 2 minutes:\n"
            "• Tweet their story\n"
            "• Sign a petition\n"
            "• Share their names\n\n"
            "👉 Start here: {link}\n\n"
            "#JusticeForMinab #MinabSchoolMassacre"
        ),
        "fa": (
            "🕯 ۱۶۸ کودک در حمله به مدرسه میناب کشته شدند.\n\n"
            "نام‌هایشان مشخص شده. عکس‌هایشان جمع‌آوری شده.\n"
            "ما داریم پرونده‌شان رو زنده نگه می‌داریم.\n\n"
            "🤲 شما هم می‌تونید کمک کنید — فقط ۲ دقیقه:\n"
            "• یک توییت بزنید\n"
            "• یک طومار امضا کنید\n"
            "• داستانشان رو به اشتراک بذارید\n\n"
            "👉 شروع کنید: {link}\n\n"
            "#JusticeForMinab #عدالت_برای_میناب"
        ),
        "ar": (
            "🕯 ١٦٨ طفلاً قُتلوا في الهجوم على مدرسة ميناب.\n\n"
            "تم التعرّف على أسمائهم. جُمعت صورهم.\n"
            "نحن نحافظ على قضيتهم حيّة.\n\n"
            "🤲 يمكنك المساعدة — دقيقتان فقط:\n"
            "• غرّد بقصتهم\n"
            "• وقّع عريضة\n"
            "• شارك أسماءهم\n\n"
            "👉 ابدأ هنا: {link}\n\n"
            "#JusticeForMinab #العدالة_لأطفال_ميناب"
        ),
    },
    "invite_memorial_sent": {
        "en": "✅ *Photo message ready!*\n\nForward the message above 👆 to your friends and contacts.\n\nEvery share helps grow the movement. 🕯",
        "fa": "✅ *پیام عکسی آماده است!*\n\nپیام بالا 👆 را برای دوستان و مخاطبانتان فوروارد کنید.\n\nهر اشتراک‌گذاری به رشد جنبش کمک می‌کند. 🕯",
        "ar": "✅ *رسالة الصورة جاهزة!*\n\nأعد توجيه الرسالة أعلاه 👆 لأصدقائك ومعارفك.\n\nكل مشاركة تساعد في نمو الحركة. 🕯",
    },
    "invite_campaign_text": {
        "en": (
            "✊ *{name}*\n\n"
            "We're a volunteer group working for accountability "
            "regarding the Minab school attack.\n\n"
            "So far we've built:\n"
            "📋 Petitions  •  🐦 Tweet campaigns  •  ✍️ Original content\n\n"
            "You can help with just 2 minutes:\n"
            "👉 {link}"
        ),
        "fa": (
            "✊ *{name}*\n\n"
            "ما یک گروه داوطلب هستیم که برای پاسخگویی "
            "درباره حمله به مدرسه میناب تلاش می‌کنیم.\n\n"
            "تا الان:\n"
            "📋 طومار  •  🐦 توییت  •  ✍️ محتوا\n\n"
            "با ۲ دقیقه وقت می‌تونید کمک کنید:\n"
            "👉 {link}"
        ),
        "ar": (
            "✊ *{name}*\n\n"
            "نحن مجموعة متطوعين نعمل من أجل المحاسبة "
            "بشأن الهجوم على مدرسة ميناب.\n\n"
            "حتى الآن:\n"
            "📋 عرائض  •  🐦 حملات تغريد  •  ✍️ محتوى أصلي\n\n"
            "يمكنك المساعدة بدقيقتين فقط:\n"
            "👉 {link}"
        ),
    },
    "btn_memorial_style": {
        "en": "🕯 Memorial — Children of Minab",
        "fa": "🕯 یادبود — کودکان میناب",
        "ar": "🕯 النصب التذكاري — أطفال ميناب",
    },
    "btn_campaign_style": {
        "en": "✊ Campaign — Join the Movement",
        "fa": "✊ کمپین — به جنبش بپیوندید",
        "ar": "✊ الحملة — انضم للحركة",
    },
    "help": {
        "en": "ℹ️ *Help — People for Peace Bot*\n\n"
              "Available commands:\n"
              "/start — Main menu\n"
              "/tasks — View available tasks\n"
              "/language — Change language\n"
              "/help — Show this help\n\n"
              "💡 Join a campaign and complete tasks to make an impact\\!",
        "fa": "ℹ️ *راهنما — ربات مردم برای صلح*\n\n"
              "دستورات موجود:\n"
              "/start — منوی اصلی\n"
              "/tasks — مشاهده وظایف\n"
              "/language — تغییر زبان\n"
              "/help — نمایش راهنما\n\n"
              "💡 به یک کمپین بپیوندید و با انجام وظایف تأثیرگذار باشید\\!",
        "ar": "ℹ️ *المساعدة — بوت الناس من أجل السلام*\n\n"
              "الأوامر المتاحة:\n"
              "/start — القائمة الرئيسية\n"
              "/tasks — عرض المهام\n"
              "/language — تغيير اللغة\n"
              "/help — عرض المساعدة\n\n"
              "💡 انضم إلى حملة وأكمل المهام لإحداث تأثير\\!",
    },
    "btn_video_style": {
        "en": "🎬 Video — 100 Faces of Peace",
        "fa": "🎬 ویدیو — صد چهره‌ی صلح",
        "ar": "🎬 فيديو — مئة وجه للسلام",
    },
    "invite_video_caption": {
        "en": (
            "🎬 Memorial video — Children of Minab\n\n"
            "This video shows the faces of 100 children killed "
            "in the attack on their school.\n"
            "We've collected every name and every story.\n\n"
            "Watch, and if you want to help:\n"
            "👉 {link}\n\n"
            "Just 2 minutes. A tweet or a signature."
        ),
        "fa": (
            "🎬 ویدیوی یادبود کودکان میناب\n\n"
            "این ویدیو چهره‌ی ۱۰۰ کودکی رو نشون می‌ده "
            "که تو حمله به مدرسه‌شون کشته شدند.\n"
            "ما اسم و داستان تک‌تکشون رو جمع کردیم.\n\n"
            "ببینید و اگه دلتون خواست کمک کنید:\n"
            "👉 {link}\n\n"
            "فقط ۲ دقیقه. یک توییت یا یک امضا."
        ),
        "ar": (
            "🎬 فيديو تذكاري — أطفال ميناب\n\n"
            "يعرض هذا الفيديو وجوه ١٠٠ طفل قُتلوا "
            "في الهجوم على مدرستهم.\n"
            "جمعنا كل اسم وكل قصة.\n\n"
            "شاهدوا، وإذا أردتم المساعدة:\n"
            "👉 {link}\n\n"
            "دقيقتان فقط. تغريدة أو توقيع."
        ),
    },
    "invite_video_sent": {
        "en": "✅ *Video ready!*\n\nForward the video above 👆 to your friends and groups.\n\nLet them see the faces. Let them hear the names. 🕊",
        "fa": "✅ *ویدیو آماده است!*\n\nویدیوی بالا 👆 را برای دوستان و گروه‌هایتان فوروارد کنید.\n\nبگذارید چهره‌ها را ببینند. بگذارید نام‌ها را بشنوند. 🕊",
        "ar": "✅ *الفيديو جاهز!*\n\nأعد توجيه الفيديو أعلاه 👆 لأصدقائك ومجموعاتك.\n\nدعهم يرون الوجوه. دعهم يسمعون الأسماء. 🕊",
    },
    "invite_stats_list": {
        "en": "📨 Your Invites ({count}):",
        "fa": "📨 دعوت‌های شما ({count}):",
        "ar": "📨 دعواتك ({count}):",
    },
    "invite_stats_zero": {
        "en": "📨 No one joined yet — share your invite link\\!",
        "fa": "📨 هنوز کسی نپیوسته — لینک دعوت را به اشتراک بگذارید\\!",
        "ar": "📨 لم ينضم أحد بعد — شارك رابط دعوتك\\!",
    },
    "invite_stats_followup": {
        "en": "📊 {count} people joined through your invites. Keep sharing\\! 🚀",
        "fa": "📊 {count} نفر از طریق دعوت شما پیوسته‌اند. ادامه دهید\\! 🚀",
        "ar": "📊 {count} شخص انضموا عبر دعوتك. واصل المشاركة\\! 🚀",
    },
    "btn_change_language": {
        "en": "🌍 Change Language",
        "fa": "🌍 تغییر زبان",
        "ar": "🌍 تغيير اللغة",
    },
    "language_prompt": {
        "en": "🌍 Choose your language:",
        "fa": "🌍 زبان خود را انتخاب کنید:",
        "ar": "🌍 اختر لغتك:",
    },

    # ── Campaign About / Info ────────────────────────────────────
    "btn_about_campaign": {
        "en": "ℹ️ About This Campaign",
        "fa": "ℹ️ درباره این کمپین",
        "ar": "ℹ️ عن هذه الحملة",
    },
    "campaign_about": {
        "en": (
            "ℹ️ *About {name}*\n\n"
            "{description}\n\n"
            "👥 {members} volunteers joined\n"
            "🎯 {tasks} tasks available\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *Resources:*\n"
            "🕯 [Memorial](https://peopleforpeace.live)\n"
            "📄 [Evidence & Facts](https://peopleforpeace.live/evidence.html)\n"
            "📊 [Verified Data](https://peopleforpeace.live/data.html)\n"
            "📢 Follow: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "#️⃣ {hashtags}"
        ),
        "fa": (
            "ℹ️ *درباره {name}*\n\n"
            "{description}\n\n"
            "👥 {members} داوطلب پیوسته‌اند\n"
            "🎯 {tasks} وظیفه موجود\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *منابع:*\n"
            "🕯 [صفحه یادبود](https://peopleforpeace.live)\n"
            "📄 [شواهد و حقایق](https://peopleforpeace.live/evidence.html)\n"
            "📊 [داده‌های تأییدشده](https://peopleforpeace.live/data.html)\n"
            "📢 دنبال کنید: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "#️⃣ {hashtags}"
        ),
        "ar": (
            "ℹ️ *عن {name}*\n\n"
            "{description}\n\n"
            "👥 {members} متطوع انضموا\n"
            "🎯 {tasks} مهمة متاحة\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "🔗 *الموارد:*\n"
            "🕯 [صفحة التذكار](https://peopleforpeace.live)\n"
            "📄 [أدلة وحقائق](https://peopleforpeace.live/evidence.html)\n"
            "📊 [بيانات موثقة](https://peopleforpeace.live/data.html)\n"
            "📢 تابعنا: @people4peace\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "#️⃣ {hashtags}"
        ),
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

        t('btn_help', lang): '_route_help',
        t('btn_profile', lang): '_route_profile',
        t('btn_language', lang): '_route_language',
        t('btn_invite_friends', lang): '_route_invite',
    }


# All possible button texts across all languages (for routing)
ALL_BUTTON_ROUTES: dict[str, str] = {}
for _lang in ('en', 'fa', 'ar'):
    ALL_BUTTON_ROUTES.update(get_button_routes(_lang))
