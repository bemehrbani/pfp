/**
 * People for Peace & Justice ry (PFPJ ry) — Multimedia & Investigative Video Library Data
 * Master metadata store for all video investigations, documentary series, and audio-visual assets.
 */

const PFP_MEDIA_DATA = [
  // ==========================================
  // 1. INTERNATIONAL OSINT & VIDEO INVESTIGATIONS
  // ==========================================
  {
    id: "sky-news-investigation-evidence-points-to-us",
    sourceUrl: "https://www.youtube.com/watch?v=siRuobaj7IE&t=8s",
    slug: "sky-news-investigation-minab-attack-evidence-points-to-us",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Sky News Full Investigation: All Evidence Points to US Being Responsible",
      fa: "مستند تحقیقی اسکای نیوز: تمام شواهد نشان‌دهنده مسئولیت ارتش آمریکا است"
    },
    producer: "Sky News",
    runtime: "49:35",
    resolution: "1080p Full HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=siRuobaj7IE",
    youtubeId: "siRuobaj7IE",
    poster: "/images/sky-news-investigation.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=siRuobaj7IE",
    featured: true,
    description: {
      en: "In this comprehensive 50-minute investigative documentary, Sky News' Dominic Waghorn reports from Minab — the first major western journalist on the ground. Through forensic 3D site reconstruction, interviews with bereaved mothers and survivors, and testimony from US military whistleblowers, Sky News investigates the fatal strike on Shajareh Tayyebeh Primary School that killed 156 people, concluding all evidence points to US military responsibility.",
      fa: "در این مستند تحقیقی جامع ۵۰ دقیقه‌ای، دومینیک واگهورن خبرنگار ارشد بین‌المللی اسکای نیوز با سفر میدانی به میناب به‌عنوان نخستین خبرنگار غربی، فاجعه حمله به دبستان شجره طیبه را بررسی می‌کند. این مستند با بازسازی سه‌بعدی محل اصابت موشک، گفتگو با کودکان بازمانده و مادران داغدار، و شهادت افشاگران نظامی آمریکا، شواهدی جامع از مسئولیت ارتش ایالات متحده در شهادت ۱۵۶ غیرنظامی از جمله ۱۲۰ دانش‌آموز ارائه می‌دهد."
    },
    keyFindings: [
      "First on-the-ground investigation in Minab conducted by a major western news organization (Dominic Waghorn).",
      "3D forensic spatial reconstruction corroborating the triple-strike Tomahawk timeline and blast trajectory.",
      "Firsthand testimonies from surviving children, bereaved families, and emergency triage doctors in Hormozgan.",
      "Revelations from US defense and military whistleblowers disclosing intelligence targeting failures and strike approvals."
    ],
    tags: ["Sky News", "Dominic Waghorn", "OSINT", "Full Documentary", "Tomahawk", "School Strike", "Geneva Conventions", "Whistleblowers"]
  },
  {
    id: "minab-sky-distortion-interview",
    sourceUrl: "https://www.youtube.com/watch?v=27c0QBF-7pk",
    slug: "war-crime-or-mistake-sky-news-minab-distortion",
    category: "international",
    categoryLabel: {"en": "International Investigation", "fa": "تحقیقات بین‌المللی"},
    title: {"en": "War Crime or Mistake? How Sky Distorted the Minab School Bombing", "fa": "جنایت جنگی یا اشتباه؟ تحریف واقعه مدرسه میناب توسط رسانه‌های غربی"},
    producer: "Jedaal English (Dr. Helyeh Doutaghi & Prof. Bikrum Gill)",
    runtime: "01:28:46",
    resolution: "1080p Full HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=27c0QBF-7pk",
    youtubeId: "27c0QBF-7pk",
    poster: "/images/still-minab/sky-distortion-interview.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=27c0QBF-7pk",
    featured: true,
    description: {"en": "An in-depth critical panel featuring Dr. Helyeh Doutaghi and Prof. Bikrum Gill analyzing how Western mainstream reporting (specifically Sky News) framed the deadly strike on Shajareh Tayyebeh Primary School as an operational error rather than an egregious war crime under International Humanitarian Law.", "fa": "نشست تحلیلی و موشکافانه با حضور دکتر حلیه دوتاقی و پروفسور بیکرام گیل در نقد روایت رسانه‌های غربی (به‌ویژه اسکای نیوز) و بازنمایی حمله به دبستان دخترانه میناب به‌عنوان خطای عملیاتی به جای جنایت جنگی آشکار."},
    keyFindings: ["Critical legal and political analysis of mainstream media framing of civilian strikes.", "Detailed deconstruction of the 'targeting mistake' defense under Geneva Protocol I.", "Contextualizing the Minab massacre within broader imperial warfare and geopolitical erasure."],
    tags: ["Helyeh Doutaghi", "Bikrum Gill", "Sky News Critique", "Media Analysis", "War Crimes", "IHL", "Jedaal English"]
  },

  {
    id: "sky-news-visual-investigation",
    sourceUrl: "https://news.sky.com/topic/iran-5858",
    slug: "sky-news-investigation-minab-primary-school",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Sky News Visual Investigation: Deadly Strike on Minab Primary School",
      fa: "تحقیقات تصویری اسکای نیوز: حمله مرگبار به دبستان میناب"
    },
    producer: "Sky News",
    runtime: "06:45",
    resolution: "1080p Full HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/01_Sky_News_Visual_Investigation_Minab_School.mp4",
    poster: "/images/og-evidence.png",
    downloadUrl: "/media/international/01_Sky_News_Visual_Investigation_Minab_School.mp4",
    fileSize: "51.6 MB",
    featured: true,
    description: {
      en: "Sky News' open-source investigation team maps the strike timeline, verifies crater depth and missile fragments, and details the destruction of the Shajareh Tayyebeh School in Minab.",
      fa: "تیم تحقیقات متن‌باز (OSINT) اسکای نیوز با بازسازی زمانی حمله، تطبیق تصاویر ماهواره‌ای و ترکش‌های تاماهاک، چگونگی انهدام دبستان شجره طیبه میناب را بررسی می‌کند."
    },
    keyFindings: [
      "Satellite mapping confirmed the school was separated from military perimeters.",
      "Identified Tomahawk cruise missile fragments on-site.",
      "Corroborated 160+ casualties among elementary school students and staff."
    ],
    tags: ["OSINT", "Sky News", "Tomahawk", "School Strike", "Geneva Conventions"]
  },
  {
    id: "visual-breakdown-what-really-happened",
    sourceUrl: "https://www.youtube.com/results?search_query=Minab+School+Strike+Investigation",
    slug: "what-really-happened-minab-school-strike",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Visual Forensic Breakdown: What Really Happened at Minab?",
      fa: "کالبدشکافی تصویری: در حمله به مدرسه میناب چه گذشت؟"
    },
    producer: "Investigative Forensics Network",
    runtime: "12:18",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/02_Visual_Breakdown_What_Really_Happened_Minab.mp4",
    poster: "/images/og-evidence.png",
    downloadUrl: "/media/international/02_Visual_Breakdown_What_Really_Happened_Minab.mp4",
    fileSize: "97.8 MB",
    featured: true,
    description: {
      en: "A comprehensive spatiotemporal reconstruction examining targeting data failures, the triple-tap missile sequence, and the devastating impact on classrooms and pediatric triage units.",
      fa: "بازسازی کامل فضا-زمانی حادثه که به بررسی خطاهای زنجیره هدف‌گیری، شلیک سه مرحله‌ای موشک‌ها و خسارات وارده به کلاس‌های درس و بیمارستان میناب می‌پردازد."
    },
    keyFindings: [
      "Analysis of the outdated 2013 targeting database utilized in operational planning.",
      "Reconstruction of classroom positions relative to blast epicenter.",
      "Interviews with forensic medical specialists from Hazrat Abolfazl Hospital."
    ],
    tags: ["Forensics", "Spatiotemporal", "Targeting Failure", "Triple-Tap"]
  },
  {
    id: "bbc-news-onsite-report",
    sourceUrl: "https://www.bbc.com/news/world-middle-east",
    slug: "bbc-news-onsite-report-minab-school",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "BBC News On-Site: Inside the School Where Over 120 Children Were Killed",
      fa: "گزارش میدانی بی‌بی‌سی نیوز: از درون مدرسه‌ای که بیش از ۱۲۰ کودک در آن جان باختند"
    },
    producer: "BBC News",
    runtime: "03:40",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/03_BBC_News_OnSite_Report_Minab_School.mp4",
    poster: "/images/og-landing.png",
    downloadUrl: "/media/international/03_BBC_News_OnSite_Report_Minab_School.mp4",
    fileSize: "17.9 MB",
    featured: false,
    description: {
      en: "BBC correspondents walk through the pulverized classrooms, schoolyard ruins, and prayer room of Shajareh Tayyebeh, reporting directly on the human toll.",
      fa: "خبرنگاران بی‌بی‌سی با حضور در محل تخریب‌شده مدرسه شجره طیبه میناب، وسایل دانش‌آموزان و رنج بازماندگان را به تصویر می‌کشند."
    },
    keyFindings: [
      "Firsthand visual inspection of school supplies, books, and children's drawings in the rubble.",
      "Eyewitness accounts from teachers and surviving neighbors."
    ],
    tags: ["BBC News", "Field Report", "Victim Memorial", "Minab"]
  },
  {
    id: "sky-news-evidence-points-to-us",
    sourceUrl: "https://www.youtube.com/watch?v=siRuobaj7IE&t=8s",
    slug: "sky-news-evidence-points-to-us-strike",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Sky News Analysis: All Forensic Evidence Points to US Military Responsibility",
      fa: "گزارش تحلیلی اسکای نیوز: تمام شواهد فنی نشان‌دهنده مسئولیت ارتش آمریکا است"
    },
    producer: "Sky News",
    runtime: "04:12",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/04_Sky_News_Evidence_Points_To_US.mp4",
    poster: "/images/og-evidence.png",
    downloadUrl: "/media/international/04_Sky_News_Evidence_Points_To_US.mp4",
    fileSize: "13.4 MB",
    featured: false,
    description: {
      en: "Investigative report examining munitions serial fragments, launch attribution vectors, and official Pentagon acknowledgments regarding targeting failures in Hormozgan.",
      fa: "بررسی بقایای شماره سریال تسلیحات، خط سیر پرتاب و اعترافات مقامات دفاعی در خصوص استفاده از داده‌های منسوخ در هدف‌گیری مدرسه."
    },
    keyFindings: [
      "Verification of BGM-109 Tomahawk component serial plates.",
      "Assessment of Command Responsibility under International Humanitarian Law."
    ],
    tags: ["Munitions", "Command Responsibility", "CENTCOM", "Sky News"]
  },
  {
    id: "france24-english-investigation",
    slug: "france24-what-we-know-minab-strike",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "FRANCE 24 English: What We Know About the Strike on Minab Girls' School",
      fa: "فرانس ۲۴ انگلیسی: آنچه درباره حمله به دبستان دخترانه میناب می‌دانیم"
    },
    producer: "FRANCE 24",
    runtime: "05:10",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/05_France24_English_Minab_School_Strike.mp4",
    poster: "/images/og-landing.png",
    downloadUrl: "/media/international/05_France24_English_Minab_School_Strike.mp4",
    fileSize: "17.9 MB",
    featured: false,
    description: {
      en: "FRANCE 24 international desk provides an analytical breakdown of the diplomatic fallout, UNESCO/UNICEF statements, and calls for independent war crimes tribunals.",
      fa: "تحلیل سرویس بین‌المللی فرانس ۲۴ پیرامون پیامدهای دیپلماتیک، بیانیه‌های یونسکو و یونیسف و ضرورت پیگیری در دادگاه‌های بین‌المللی."
    },
    keyFindings: [
      "Summary of international legal condemnation by OHCHR and Safe Schools Declaration signatories.",
      "Examination of universal jurisdiction avenues in Europe."
    ],
    tags: ["FRANCE 24", "Diplomacy", "UNICEF", "Humanitarian Law"]
  },
  {
    id: "visual-analysis-us-responsible",
    sourceUrl: "https://www.youtube.com/results?search_query=Minab+school+investigation+OSINT",
    slug: "visual-analysis-us-responsible-minab",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Visual Trajectory & Geolocation: Verifying the School Strike Footage",
      fa: "تحلیل زاویه پرواز و مکان‌یابی: راستی‌آزمایی ویدیوهای اصابت به مدرسه"
    },
    producer: "OSINT Video Verification Unit",
    runtime: "05:45",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/06_Visual_Analysis_US_Responsible_Minab.mp4",
    poster: "/images/og-evidence.png",
    downloadUrl: "/media/international/06_Visual_Analysis_US_Responsible_Minab.mp4",
    fileSize: "27.6 MB",
    featured: false,
    description: {
      en: "Frame-by-frame geolocation matching terrain elevation, shadows, and acoustic sound arrival to reconstruct the incoming cruise missile velocity and impact point.",
      fa: "تطبیق فریم به فریم موقعیت جغرافیایی، سایه‌ها و سرعت صوت برای بازسازی سرعت و زاویه اصابت موشک کروز تاماهاک به مجتمع آموزشی شجره طیبه."
    },
    keyFindings: [
      "Multi-angle video synchronization confirming the exact time (08:42 AM local).",
      "Geospatial triangulation matching camera perspectives in Minab rural district."
    ],
    tags: ["Geolocation", "Chronolocation", "OSINT", "Video Analysis"]
  },
  {
    id: "forensic-analysis-targeting-protections",
    sourceUrl: "https://www.icrc.org/en/war-and-law/treaties-customary-law/geneva-conventions",
    slug: "forensic-analysis-targeting-protections-ihl",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Targeting Protections & IHL: Why Was a Civilian Primary School Struck?",
      fa: "اصول حفاظت حقوق بین‌الملل: چرا یک دبستان غیرنظامی مورد اصابت قرار گرفت؟"
    },
    producer: "International Law & Accountability Forum",
    runtime: "04:35",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/07_Forensic_Analysis_Why_Target_School_In_Iran.mp4",
    poster: "/images/og-evidence.png",
    downloadUrl: "/media/international/07_Forensic_Analysis_Why_Target_School_In_Iran.mp4",
    fileSize: "15.0 MB",
    featured: false,
    description: {
      en: "A legal examination into the Geneva Conventions Additional Protocol I (Article 57 - Precautions in Attack) and how civilian harm mitigation was dismantled prior to the operation.",
      fa: "بررسی حقوقی پروتکل اول الحاقی کنوانسیون‌های ژنو (ماده ۵۷ - اقدامات احتیاطی) و نقض قوانین تفکیک اهداف غیرنظامی در حمله به مدرسه."
    },
    keyFindings: [
      "Failure of Duty of Constant Care and verification obligations.",
      "Legal precedents supporting universal jurisdiction filings in Nordic jurisdictions."
    ],
    tags: ["IHL", "Geneva Conventions", "Duty of Precaution", "Legal Analysis"]
  },
  {
    id: "minab-grieving-families-report",
    slug: "minab-school-attack-families-grieving",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Field Report: The Grieving Families and Mothers of Minab",
      fa: "گزارش میدانی: روایت رنج مادران و خانواده‌های داغدار میناب"
    },
    producer: "International Press Network",
    runtime: "03:15",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/08_Minab_Families_Grieving_English_Report.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/international/08_Minab_Families_Grieving_English_Report.mp4",
    fileSize: "15.5 MB",
    featured: false,
    description: {
      en: "A poignant English-language report documenting the grief of mothers who lost multiple children, recounting their dreams, drawings, and unfinished lives.",
      fa: "گزارشی به زبان انگلیسی که رنج مادران داغدیده، آرزوهای نقاشی‌شده کودکان و سوگ بی‌پایان خانواده‌ها در میناب را بازگو می‌کند."
    },
    keyFindings: [
      "Profiles of young student athletes including gymnast Tara Hajimiri.",
      "Interviews with surviving teachers and healthcare workers."
    ],
    tags: ["Mothers of Minab", "Human Stories", "Memorial", "Oral History"]
  },
  {
    id: "un-reactions-accountability",
    slug: "un-reactions-accountability-brief",
    category: "international",
    categoryLabel: { en: "International Investigation", fa: "تحقیقات بین‌المللی" },
    title: {
      en: "Diplomatic & UN Brief: Global Demands for Minab Accountability",
      fa: "خلاصه دیپلماتیک سازمان ملل: مطالبات جهانی برای دادخواهی فاجعه میناب"
    },
    producer: "UN Affairs Bureau",
    runtime: "08:15",
    resolution: "1080p HD",
    language: "English",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/international/10_Minab_School_Strike_UN_Reactions.mp4",
    poster: "/images/og-landing.png",
    downloadUrl: "/media/international/10_Minab_School_Strike_UN_Reactions.mp4",
    fileSize: "39.3 MB",
    featured: false,
    description: {
      en: "Overview of international reactions from UN Special Rapporteurs, OHCHR statements, and the 46 US Senators demanding transparency on AI targeting tools and civilian safeguards.",
      fa: "مروری بر مواضع گزارشگران سازمان ملل، کمیساریای عالی حقوق بشر و نامه سناتورهای آمریکایی در خصوص شفاف‌سازی خطاهای ابزارهای هدف‌گیری."
    },
    keyFindings: [
      "Formal statements from OHCHR declaring attacks on schools a grave violation.",
      "Congressional inquiry demands regarding the dismantling of civilian casualty mitigation units."
    ],
    tags: ["United Nations", "OHCHR", "Senate Inquiry", "Accountability"]
  },

  // ==========================================
  // 2. FARSI DOCUMENTARIES & FIELD REPORTS
  // ==========================================
  {
    id: "javad-mogoei-truth-of-minab",
    sourceUrl: "https://t.me/javadmogoei/821",
    slug: "javad-mogoei-truth-of-minab-english-sub",
    category: "farsi_reports",
    categoryLabel: { en: "Field Documentary", fa: "مستند میدانی" },
    title: {
      en: "The Truth of Minab (English Subtitled Edition) — By Javad Mogoei",
      fa: "مستند «حقیقت میناب» (نسخه با زیرنویس انگلیسی) — به‌روایت جواد موگویی"
    },
    producer: "Javad Mogoei (ماجرای جنگ ۲، روایت سیزدهم)",
    runtime: "11:26",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/farsi/03_Javad_Mogoei_Haghighat_Minab_English_Sub.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/farsi/03_Javad_Mogoei_Haghighat_Minab_English_Sub.mp4",
    fileSize: "35.9 MB",
    featured: true,
    description: {
      en: "Documentary filmmaker Javad Mogoei travels to Minab following the school strike, conducting firsthand interviews with surviving staff, rescuers, and mothers who lost their children in the double-tap blast sequence.",
      fa: "جواد موگویی با حضور در محل فاجعه مدرسه میناب، روایتی میدانی و بی‌واسطه از نجات‌یافتگان، امدادگران و مادرانی که برای بردن فرزندانشان آمده بودند و در شلیک دوم جان باختند ارائه می‌دهد."
    },
    keyFindings: [
      "Hardcoded English subtitles making it accessible to international audiences and researchers.",
      "Eyewitness confirmation of the interval between the first and secondary missile strikes.",
      "Deep personal accounts of maternal grief and family losses in Minab."
    ],
    tags: ["Javad Mogoei", "English Subtitles", "Field Documentary", "Mothers of Minab"]
  },
  {
    id: "nardeban-mostanad-special",
    slug: "nardeban-mostanad-channel-minab-special",
    category: "farsi_reports",
    categoryLabel: { en: "Field Documentary", fa: "مستند میدانی" },
    title: {
      en: "Mostanad Channel: 'Nardeban' Field Documentary Special",
      fa: "شبکه مستند: ویژه برنامه و مستند میدانی «نردبان» در میناب"
    },
    producer: "IRIB Mostanad Channel (شبکه مستند)",
    runtime: "14:15",
    resolution: "1080p HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/farsi/01_Nardeban_Mostanad_Special.mp4",
    poster: "/images/og-landing.png",
    downloadUrl: "/media/farsi/01_Nardeban_Mostanad_Special.mp4",
    fileSize: "47.0 MB",
    featured: false,
    description: {
      en: "Photojournalists and documentary filmmakers travel to Hormozgan to capture the immediate aftermath, first responder testimonies, and hospital emergency operations.",
      fa: "مستندسازان و عکاسان مستند با سفر به استان هرمزگان و شهرستان میناب، عملیات امداد، ثبت شواهد و روایت‌های بیمارستان حضرت ابوالفضل را مستند می‌کنند."
    },
    keyFindings: [
      "Coverage of Red Crescent rapid response recovery teams.",
      "Photographic records of the crater and structural collapse."
    ],
    tags: ["Nardeban", "Mostanad Channel", "Photojournalism", "First Responders"]
  },
  {
    id: "minab-school-news-report",
    slug: "minab-school-field-news-report",
    category: "farsi_reports",
    categoryLabel: { en: "Field Documentary", fa: "مستند میدانی" },
    title: {
      en: "Field Broadcast: Ground Footage from Shajareh Tayyebeh",
      fa: "گزارش تصویری میدانی از دبستان شجره طیبه میناب"
    },
    producer: "Regional Field Correspondents",
    runtime: "04:50",
    resolution: "1080p HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/farsi/02_Minab_School_Report.mp4",
    poster: "/images/og-landing.png",
    downloadUrl: "/media/farsi/02_Minab_School_Report.mp4",
    fileSize: "12.0 MB",
    featured: false,
    description: {
      en: "High-resolution broadcast footage capturing emergency search and rescue teams digging through rubble to recover students and teachers.",
      fa: "تصاویر با کیفیت بالا از عملیات امدادگران هلال احمر، آواربرداری و وضعیت کادر درمانی در ساعات اولیه پس از حمله موشکی."
    },
    keyFindings: [
      "Emergency rescue operations footage.",
      "Interviews with initial on-site rescuers and parents."
    ],
    tags: ["Field Report", "Search & Rescue", "Hormozgan"]
  },

  // ==========================================
  // 3. "STILL, MINAB" (هنوز میناب) — 8-PART FIELDWORK ETHNOGRAPHY MINI-SERIES
  // ==========================================
  {
    id: "still-minab-ep01",
    sourceUrl: "https://www.youtube.com/watch?v=RYd8ePRlq1U",
    slug: "still-minab-ep01-the-angels-games",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 1,
    title: {"en": "Still, Minab — Ep. 01: The Angels' Games", "fa": "هنوز میناب — قسمت ۱: بازی فرشته‌ها"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "15:16",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=RYd8ePRlq1U",
    youtubeId: "RYd8ePRlq1U",
    poster: "/images/still-minab/ep01.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=RYd8ePRlq1U",
    featured: true,
    description: {"en": "Episode One of Dr. Helyeh Doutaghi's fieldwork ethnography follows eleven-year-old Parastesh Zaeri, a survivor of the Shajareye Tayebe School bombing in Minab who does not yet know her nine-year-old brother was killed.", "fa": "قسمت اول از مجموعه مردم‌نگاری میدانی دکتر حلیه دوتاقی که سرگذشت پرستش زائری، دختر ۱۱ ساله نجات‌یافته از بمباران دبستان شجره طیبه میناب را روایت می‌کند که هنوز از شهادت برادر ۹ ساله‌اش بی‌خبر است."},
    keyFindings: ["Fieldwork ethnography documenting personal testimonies from surviving children in Minab.", "Account of Parastesh Zaeri and the psychological reality of children surviving the triple-tap strike.", "Researched, written, and narrated by Dr. Helyeh Doutaghi; directed by Ali Farirzade."],
    tags: ["Still Minab", "Helyeh Doutaghi", "Jedaal English", "Parastesh Zaeri", "Episode 1", "Children of Minab"]
  },
  {
    id: "still-minab-ep02",
    sourceUrl: "https://www.youtube.com/watch?v=iF1663_LL_I",
    slug: "still-minab-ep02-sweet-dreams-mommy",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 2,
    title: {"en": "Still, Minab — Ep. 02: Sweet Dreams, Mommy", "fa": "هنوز میناب — قسمت ۲: خواب‌های شیرین، مادر"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "20:18",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=iF1663_LL_I",
    youtubeId: "iF1663_LL_I",
    poster: "/images/still-minab/ep02.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=iF1663_LL_I",
    featured: false,
    description: {"en": "Documents the profound maternal grief, familial trauma, and unfinished lives in Minab following the three cruise missile strikes on the primary school.", "fa": "ثبت رنج عمیق مادران داغدار، تروماهای خانوادگی و خاطرات ناتمام به‌جا مانده از کودکان شهید دبستان شجره طیبه میناب."},
    tags: ["Still Minab", "Helyeh Doutaghi", "Mothers of Minab", "Episode 2", "Fieldwork"]
  },
  {
    id: "still-minab-ep03",
    sourceUrl: "https://www.youtube.com/watch?v=uWFNHw0sVT0",
    slug: "still-minab-ep03-last-dance",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 3,
    title: {"en": "Still, Minab — Ep. 03: Last Dance", "fa": "هنوز میناب — قسمت ۳: آخرین رقص"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "18:14",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=uWFNHw0sVT0",
    youtubeId: "uWFNHw0sVT0",
    poster: "/images/still-minab/ep03.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=uWFNHw0sVT0",
    featured: false,
    description: {"en": "Explores the innocent childhood aspirations, joyful moments, and artistic dreams of the young schoolchildren in Minab before the attack.", "fa": "روایتی از آرزوهای معصومانه، لحظات شاد و امیدهای کودکان دبستان میناب پیش از وقوع فاجعه بمباران."},
    tags: ["Still Minab", "Childhood Dreams", "Helyeh Doutaghi", "Episode 3"]
  },
  {
    id: "still-minab-ep04",
    sourceUrl: "https://www.youtube.com/watch?v=DywsmADbxV8",
    slug: "still-minab-ep04-the-second-explosion",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 4,
    title: {"en": "Still, Minab — Ep. 04: The Second Explosion", "fa": "هنوز میناب — قسمت ۴: انفجار دوم"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "17:43",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=DywsmADbxV8",
    youtubeId: "DywsmADbxV8",
    poster: "/images/still-minab/ep04.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=DywsmADbxV8",
    featured: false,
    description: {"en": "Examines the devastating secondary strike that hit as parents and first responders rushed to the school to rescue children trapped in rubble.", "fa": "بررسی اصابت موشک دوم در الگوی حمله متوالی که هم‌زمان با هجوم والدین و امدادگران برای نجات کودکان از زیر آوار صورت گرفت."},
    keyFindings: ["Firsthand eyewitness corroboration of the secondary missile strike timing.", "Testimonies from parents struck while searching for their daughters at the school perimeter."],
    tags: ["Still Minab", "Second Strike", "Double Tap", "First Responders", "Episode 4"]
  },
  {
    id: "still-minab-ep05",
    sourceUrl: "https://www.youtube.com/watch?v=DdulnBe_nZw",
    slug: "still-minab-ep05-from-now-on-i-want-to-live",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 5,
    title: {"en": "Still, Minab — Ep. 05: From Now On, I Want to Live", "fa": "هنوز میناب — قسمت ۵: از این به بعد می‌خواهم زندگی کنم"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "18:59",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=DdulnBe_nZw",
    youtubeId: "DdulnBe_nZw",
    poster: "/images/still-minab/ep05.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=DdulnBe_nZw",
    featured: false,
    description: {"en": "Follows surviving students through their medical rehabilitation, physical recovery, and the communal determination to persevere.", "fa": "پیگیری روند درمان و بازتوانی جسمی کودکان بازمانده و اراده جمعی جامعه میناب برای تداوم زندگی و مقاومت."},
    tags: ["Still Minab", "Rehabilitation", "Survivors", "Resilience", "Episode 5"]
  },
  {
    id: "still-minab-ep06",
    sourceUrl: "https://www.youtube.com/watch?v=mo7Nd-FN8zI",
    slug: "still-minab-ep06-who-knows-where-minab-is",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 6,
    title: {"en": "Still, Minab — Ep. 06: Who Knows Where Minab Is?", "fa": "هنوز میناب — قسمت ۶: چه کسی می‌داند میناب کجاست؟"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "22:56",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=mo7Nd-FN8zI",
    youtubeId: "mo7Nd-FN8zI",
    poster: "/images/still-minab/ep06.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=mo7Nd-FN8zI",
    featured: false,
    description: {"en": "An ethnographic inquiry into geographical marginalization, international silence, and how imperial warfare treats distant civilian populations as collateral.", "fa": "بررسی مردم‌نگارانه حاشیه‌رانی جغرافیایی، سکوت مجامع جهانی و نادیده گرفتن حقوق انسانی غیرنظامیان در محاسبات جنگی قدرت‌ها."},
    tags: ["Still Minab", "Geography", "Imperialism", "Helyeh Doutaghi", "Episode 6"]
  },
  {
    id: "still-minab-ep07",
    sourceUrl: "https://www.youtube.com/watch?v=IIJMnpLrE2U",
    slug: "still-minab-ep07-stubborn-and-patient",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 7,
    title: {"en": "Still, Minab — Ep. 07: Stubborn and Patient", "fa": "هنوز میناب — قسمت ۷: سرسخت و شکیبا"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "22:15",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=IIJMnpLrE2U",
    youtubeId: "IIJMnpLrE2U",
    poster: "/images/still-minab/ep07.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=IIJMnpLrE2U",
    featured: false,
    description: {"en": "Documents the steadfastness and dignity of Hormozgan families refusing to let their children's memory be erased or distorted in geopolitical narratives.", "fa": "روایتی از پایداری و وقار خانواده‌های هرمزگان در صیانت از یاد و نام فرزندانشان در برابر تحریف‌های رسانه‌ای و تاریخی."},
    tags: ["Still Minab", "Patience", "Dignity", "Oral History", "Episode 7"]
  },
  {
    id: "still-minab-ep08",
    sourceUrl: "https://www.youtube.com/watch?v=4YKS-aPUGIk",
    slug: "still-minab-ep08-this-is-not-a-military-zone",
    category: "still_minab",
    categoryLabel: {"en": "Still, Minab Series", "fa": "مجموعه مستند «هنوز میناب»"},
    episodeNumber: 8,
    title: {"en": "Still, Minab — Ep. 08: This Is Not a Military Zone", "fa": "هنوز میناب — قسمت ۸: اینجا منطقه نظامی نیست"},
    producer: "Dr. Helyeh Doutaghi / Jedaal English",
    runtime: "27:20",
    resolution: "1080p Full HD",
    language: "English / Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "https://www.youtube.com/watch?v=4YKS-aPUGIk",
    youtubeId: "4YKS-aPUGIk",
    poster: "/images/still-minab/ep08.jpg",
    downloadUrl: "https://www.youtube.com/watch?v=4YKS-aPUGIk",
    featured: true,
    description: {"en": "The series finale systematically refutes assertions of military proximity, proving Shajareye Tayebe was exclusively an elementary school filled with children.", "fa": "قسمت پایانی مجموعه: ابطال قطعی هرگونه ادعای نزدیکی به اهداف نظامی و اثبات هویت کاملاً آموزشی و غیرنظامی دبستان شجره طیبه میناب."},
    keyFindings: ["Conclusive spatial and photographic refutation of military proximity claims.", "Documentation of complete civilian demographics and physical school infrastructure."],
    tags: ["Still Minab", "Finale", "Civilian Infrastructure", "Geneva Conventions", "Episode 8"]
  },

  // ==========================================
  // 4. 12-EPISODE DOCUMENTARY SERIES: "قصه‌های ناتمام میناب"
  // ==========================================
  {
    id: "aparat-series-ep01",
    slug: "unfinished-tales-minab-ep01",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 1,
    title: {
      en: "Unfinished Tales of Minab — Ep. 01: The Sorrowful Tale of Minab",
      fa: "قصه‌های ناتمام میناب — قسمت ۱: قصهٔ پر غصهٔ میناب"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "02:18",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/01_قصهٔ_پر_غصهٔ_میناب؛_قسمت_اول.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/01_قصهٔ_پر_غصهٔ_میناب؛_قسمت_اول.mp4",
    fileSize: "40.2 MB",
    featured: false,
    description: {
      en: "Episode 1 introduces the peaceful coastal town of Minab and the tragic morning of February 28, 2026 when the elementary school was struck.",
      fa: "قسمت اول مجموعه به معرفی شهر آرام میناب و صبح فاجعه‌بار ۹ اسفند ۱۴۰۴ در دبستان شجره طیبه می‌پردازد."
    },
    tags: ["Series", "MADAAR TV", "Minab Stories", "Episode 1"]
  },
  {
    id: "aparat-series-ep02",
    slug: "unfinished-tales-minab-ep02",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 2,
    title: {
      en: "Unfinished Tales of Minab — Ep. 02: Messages on the Classroom Wall",
      fa: "قصه‌های ناتمام میناب — قسمت ۲: نوشته پرمعنای بچه‌ها روی دیوار کلاس"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "02:05",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/02_قسمت_دوم_مستند_قصه_میناب؛_نوشته_پرمعنای_بچه‌های_مینابی_روی_دیوار_کلاس.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/02_قسمت_دوم_مستند_قصه_میناب؛_نوشته_پرمعنای_بچه‌های_مینابی_روی_دیوار_کلاس.mp4",
    fileSize: "16.8 MB",
    featured: false,
    description: {
      en: "Examines the poignant drawings, poems, and handwritten messages left by students on the classroom blackboards before the blast.",
      fa: "بررسی دست‌نوشته‌ها، نقاشی‌ها و آرزوهای بر جای مانده از کودکان روی تخته سیاه و دیوارهای ویران‌شده کلاس."
    },
    tags: ["Series", "Classroom Memories", "MADAAR TV", "Episode 2"]
  },
  {
    id: "aparat-series-ep03",
    slug: "unfinished-tales-minab-ep03",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 3,
    title: {
      en: "Unfinished Tales of Minab — Ep. 03: The Engraved Ring",
      fa: "قصه‌های ناتمام میناب — قسمت ۳: انگشترِ نشان"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "05:12",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/03_قسمت_سوم_مستند_قصه_میناب،_انگشترِ_نشان.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/03_قسمت_سوم_مستند_قصه_میناب،_انگشترِ_نشان.mp4",
    fileSize: "45.1 MB",
    featured: false,
    description: {
      en: "Recounts the identification of teachers and staff through personal items and keepsake rings amidst the rubble.",
      fa: "روایتی از معلمان فداکار دبستان و شناسایی هویت آن‌ها از طریق وسایل شخصی و انگشترهای نشان در آوار."
    },
    tags: ["Series", "Teachers", "Identification", "Episode 3"]
  },
  {
    id: "aparat-series-ep04",
    slug: "unfinished-tales-minab-ep04",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 4,
    title: {
      en: "Unfinished Tales of Minab — Ep. 04: The School Choir Soloist",
      fa: "قصه‌های ناتمام میناب — قسمت ۴: تک‌خوان گروه سرود مدرسه"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "05:41",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/04_قسمت_چهارم_مستند_قصه_میناب؛_تک_خوان_گروه_سرود_مدرسه.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/04_قسمت_چهارم_مستند_قصه_میناب؛_تک_خوان_گروه_سرود_مدرسه.mp4",
    fileSize: "38.3 MB",
    featured: false,
    description: {
      en: "The story of the talented young girl who led the school choir and sang songs of peace and unity across Hormozgan.",
      fa: "سرگذشت دختر هنرمندی که تک‌خوان گروه سرود مدرسه بود و نغمه‌های صلح و امید را در هرمزگان سر می‌داد."
    },
    tags: ["Series", "Choir", "Youth Dreams", "Episode 4"]
  },
  {
    id: "aparat-series-ep05",
    slug: "unfinished-tales-minab-ep05",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 5,
    title: {
      en: "Unfinished Tales of Minab — Ep. 05: The Final Goodbye",
      fa: "قصه‌های ناتمام میناب — قسمت ۵: خداحافظی آخر"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "05:25",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/05_مستند_پنجم_قصه_میناب؛_خداحافظی_آخر.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/05_مستند_پنجم_قصه_میناب؛_خداحافظی_آخر.mp4",
    fileSize: "40.5 MB",
    featured: false,
    description: {
      en: "Mothers and fathers recount the last morning routines, breakfast tables, and goodbye hugs before sending their children to school.",
      fa: "خاطرات والدین از آخرین صبحانه، بستن بند کفش‌ها و آخرین نگاه‌ها پیش از رفتن کودکان به مدرسه."
    },
    tags: ["Series", "Morning Farewells", "Family Grief", "Episode 5"]
  },
  {
    id: "aparat-series-ep06",
    slug: "unfinished-tales-minab-ep06",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 6,
    title: {
      en: "Unfinished Tales of Minab — Ep. 06: Fatemeh Zahra and Her Mother",
      fa: "قصه‌های ناتمام میناب — قسمت ۶: فاطمه‌زهرا و مادرش"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "03:53",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/06_قسمت_ششم_مستند_قصه_میناب؛_فاطمه_زهرا_و_مادرش.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/06_قسمت_ششم_مستند_قصه_میناب؛_فاطمه_زهرا_و_مادرش.mp4",
    fileSize: "35.6 MB",
    featured: false,
    description: {
      en: "Documents the tragic martyrdom of mother and daughter who were struck together at the school gate during the secondary explosion.",
      fa: "روایت شهادت مظلومانه مادری که برای حفاظت از دخترش فاطمه‌زهرا شتافت و هر دو در کنار هم به شهادت رسیدند."
    },
    tags: ["Series", "Mother and Child", "Mothers of Minab", "Episode 6"]
  },
  {
    id: "aparat-series-ep07",
    slug: "unfinished-tales-minab-ep07",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 7,
    title: {
      en: "Unfinished Tales of Minab — Ep. 07: Five Children From One Family",
      fa: "قصه‌های ناتمام میناب — قسمت ۷: ماجرای پیدا شدن پنج شهید از یک خانواده"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "05:08",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/07_قسمت_هفتم_مستند_قصه_میناب؛_ماجرای_پیدا_شدن_پنج_شهید_از_یک_خانواده.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/07_قسمت_هفتم_مستند_قصه_میناب؛_ماجرای_پیدا_شدن_پنج_شهید_از_یک_خانواده.mp4",
    fileSize: "33.5 MB",
    featured: false,
    description: {
      en: "The devastating story of the Salari/Zakeri family clans who lost five young siblings and cousins in a single instant.",
      fa: "روایت جانسوز خاندان‌های زاکری و سالاری که پنج کودک و نوجوان از یک خانواده را در یک لحظه از دست دادند."
    },
    tags: ["Series", "Family Clans", "Salari", "Zakeri", "Episode 7"]
  },
  {
    id: "aparat-series-ep08",
    slug: "unfinished-tales-minab-ep08",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 8,
    title: {
      en: "Unfinished Tales of Minab — Ep. 08: The Motorcyclist Rescuer",
      fa: "قصه‌های ناتمام میناب — قسمت ۸: کار جالب موتورسوار بامعرفت مینابی در روز حادثه"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "04:30",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/08_قسمت_هشتم_مستند_قصه_میناب؛_کار_جالب_موتور_سوار_بامعرفت_مینابی_در_روز_حادثه.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/08_قسمت_هشتم_مستند_قصه_میناب؛_کار_جالب_موتور_سوار_بامعرفت_مینابی_در_روز_حادثه.mp4",
    fileSize: "29.8 MB",
    featured: false,
    description: {
      en: "Chronicles the bravery of local residents who rushed into burning dust with motorcycles and personal vehicles to evacuate injured students.",
      fa: "فداکاری مردم محلی میناب که با موتورسیکلت و خودروهای شخصی، کودکان مجروح را زیر آتش به بیمارستان رساندند."
    },
    tags: ["Series", "Civic Bravery", "Rescuers", "Episode 8"]
  },
  {
    id: "aparat-series-ep09",
    slug: "unfinished-tales-minab-ep09",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 9,
    title: {
      en: "Unfinished Tales of Minab — Ep. 09: Portrait of Hope",
      fa: "قصه‌های ناتمام میناب — قسمت ۹: تصویر امید"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "01:21",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/09_قسمت_نهم_مستند_میناب.تصویر_امید.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/09_قسمت_نهم_مستند_میناب.تصویر_امید.mp4",
    fileSize: "11.4 MB",
    featured: false,
    description: {
      en: "Focuses on the surviving children, pediatric recovery, and the resilient spirit of the teachers who returned to teach in temporary tents.",
      fa: "روایتی از مقاومت کودکان بازمانده، تلاش کادر درمانی و برپایی کلاس‌های درس در چادرهای موقت."
    },
    tags: ["Series", "Resilience", "Hope", "Surviving Children", "Episode 9"]
  },
  {
    id: "aparat-series-ep10",
    slug: "unfinished-tales-minab-ep10",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 10,
    title: {
      en: "Unfinished Tales of Minab — Ep. 10: The Moral Bankruptcy",
      fa: "قصه‌های ناتمام میناب — قسمت ۱۰: ورشکستگی اخلاقی"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "01:14",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/10_قسمت_دهم_مستند_میناب.ورشکستگی_آمریکا.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/10_قسمت_دهم_مستند_میناب.ورشکستگی_آمریکا.mp4",
    fileSize: "11.4 MB",
    featured: false,
    description: {
      en: "Examines the legal, political, and moral implications of modern standoff warfare that sacrifices civilian lives under algorithmic targeting negligence.",
      fa: "تحلیلی بر ورشکستگی اخلاقی و مسئولیت حقوقی جنگ‌افزارهای دورایستا و خطاهای فاجعه‌بار هوش مصنوعی در هدف‌گیری غیرنظامیان."
    },
    tags: ["Series", "Accountability", "Moral Responsibility", "Episode 10"]
  },
  {
    id: "aparat-series-ep11",
    slug: "unfinished-tales-minab-ep11",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 11,
    title: {
      en: "Unfinished Tales of Minab — Ep. 11: A Common Language",
      fa: "قصه‌های ناتمام میناب — قسمت ۱۱: زبان مشترک"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "01:51",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/11_قسمت_یازدهم_مستند_میناب_زبان_مشترک.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/11_قسمت_یازدهم_مستند_میناب_زبان_مشترک.mp4",
    fileSize: "16.5 MB",
    featured: false,
    description: {
      en: "Explores how universal empathy and solidarity unite parents, activists, and international communities across borders in shared sorrow for innocent children.",
      fa: "چگونگی پیوند همدلی و همبستگی جهانی میان انسان‌ها در دفاع از حق حیات کودکان فراتر از مرزها."
    },
    tags: ["Series", "Global Solidarity", "Human Rights", "Episode 11"]
  },
  {
    id: "aparat-series-ep12",
    slug: "unfinished-tales-minab-ep12",
    category: "series_minab",
    categoryLabel: { en: "Documentary Series", fa: "مجموعه مستند ۱۲ قسمتی" },
    episodeNumber: 12,
    title: {
      en: "Unfinished Tales of Minab — Ep. 12 (Finale): Lullabies at the Graves",
      fa: "قصه‌های ناتمام میناب — قسمت ۱۲ (پایانی): لالایی مادران بر سر مزار کودکان"
    },
    producer: "MADAAR TV (رسانه تصویری مدار)",
    runtime: "04:03",
    resolution: "1080p Full HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/series/12_قسمت_پایانی_مستند_میناب_قصه_های_ناتمام_میناب.mp4",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/series/12_قسمت_پایانی_مستند_میناب_قصه_های_ناتمام_میناب.mp4",
    fileSize: "63.8 MB",
    featured: true,
    description: {
      en: "The emotional climax of the series: mothers singing traditional coastal lullabies over the memorial flower plots at Minab Martyrs' Cemetery.",
      fa: "پایان‌بخش مجموعه مستند: زمزمه‌های جانسوز و لالایی‌های محلی مادران بر مزار کودکان در گلزار شهدای میناب."
    },
    tags: ["Series", "Lullabies", "Cemetery Memorial", "Finale", "Episode 12"]
  },

  // ==========================================
  // 5. FEATURE DOCUMENTARY PROFILES (CINEMA & FESTIVALS)
  // ==========================================
  {
    id: "hoda-documentary-profile",
    slug: "hoda-documentary-hamed-saadat",
    category: "documentary_profiles",
    categoryLabel: { en: "Feature Cinema", fa: "سینمای مستند" },
    title: {
      en: "Documentary 'Hoda' (هدا) — Directed by Hamed Saadat",
      fa: "مستند بلند «هدا» — به کارگردانی حامد سعادت"
    },
    producer: "Documentary, Experimental and Animation Film Center (DEFC)",
    runtime: "Festival Feature",
    resolution: "4K Master / Cinema Verite",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: null, // Festival screener via outreach
    poster: "/images/og-memorial.png",
    downloadUrl: null,
    outreachLetter: "/screening_media/OUTREACH_HODA_DOCUMENTARY.md",
    featured: true,
    description: {
      en: "A character-driven cinematic documentary following 'Hoda', a young girl who survived the Shajareh Tayyebeh bombing after hours trapped beneath rubble, portraying the enduring trauma and courage of surviving children.",
      fa: "اثری سینمایی و عمیق درباره «هدا»، دختر دانش‌آموزی که پس از ساعت‌ها از زیر آوار زنده نجات یافت و روایتگر رنج‌های ادامه‌دار و آسیب‌های جسمی و روانی کودکان بازمانده است."
    },
    keyFindings: [
      "Official production by Iran's DEFC (مرکز گسترش سینمای مستند).",
      "Focuses on surviving children's psychological healing and long-term care.",
      "Outreach template available in the screening hub for international NGO screening authorization."
    ],
    tags: ["Hoda", "Hamed Saadat", "DEFC", "Cinema Verite", "Feature Documentary"]
  },
  {
    id: "minab-hazer-ammar-profile",
    sourceUrl: "https://ammaryar.ir/m/xrrob",
    slug: "minab-hazer-documentary",
    category: "documentary_profiles",
    categoryLabel: { en: "Feature Cinema", fa: "سینمای مستند" },
    title: {
      en: "Documentary 'Minab; Hazer' (میناب؛ حاضر)",
      fa: "مستند «میناب؛ حاضر» (روایت یک جنگ)"
    },
    producer: "Alireza Zarei / Ammar Film Festival (عماریار)",
    runtime: "48:21",
    resolution: "720p HD",
    language: "Farsi",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/farsi/04_Minab_Hazer_Documentary.mp4",
    poster: "/images/minab-hazer-poster.jpg",
    downloadUrl: "/media/farsi/04_Minab_Hazer_Documentary.mp4",
    fileSize: "395 MB",
    outreachLetter: "/screening_media/OUTREACH_MINAB_HAZER_DOCUMENTARY.md",
    featured: true,
    description: {
      en: "Directed by Alireza Zarei and produced by Morteza Akhoundi under the Ammar Film Festival archive, this 48-minute feature documentary chronicles the February 28, 2026 strike on Shajareh Tayyebeh Primary School in Minab through firsthand survivor testimonies, family accounts, and ground footage from Hormozgan.",
      fa: "مستند بلند ۴۸ دقیقه‌ای «میناب؛ حاضر» به کارگردانی علیرضا زارعی و تهیه‌کنندگی مرتضی آخوندی، روایتی میدانی و جامع از فاجعه حمله ۹ اسفند ۱۴۰۴ به دبستان شجره طیبه میناب، شهادت دانش‌آموزان و معلمان، و روایت‌های دست اول خانواده‌ها و شاهدان عینی در هرمزگان است."
    },
    keyFindings: [
      "Full 48-minute feature documentary directed by Alireza Zarei and produced by Morteza Akhoundi.",
      "On-the-ground testimonies from bereaved parents, surviving classmates, and emergency responders in Minab.",
      "Visual documentation of destroyed classrooms, children's schoolbooks, and community mourning ceremonies."
    ],
    tags: ["Ammar Film", "Minab Hazer", "Alireza Zarei", "Feature Documentary"]
  },

  // ==========================================
  // 6. AUDIO ORAL HISTORIES & SOUNDTRACKS
  // ==========================================
  {
    id: "melody-of-peace-score",
    sourceUrl: "https://peopleforpeace.live/media/audio/01_Melody_of_Peace.ogg",
    slug: "melody-of-peace-official-soundtrack",
    category: "audio_memorials",
    categoryLabel: { en: "Audio & Score", fa: "موسیقی و نواهای صلح" },
    title: {
      en: "Melody of Peace (Nava-ye Solh) — Official Memorial Score",
      fa: "موسیقی یادبود «نوای صلح» — ملودی اختصاصی کودکان میناب"
    },
    producer: "People for Peace & Justice ry",
    runtime: "03:45",
    resolution: "High-Fidelity Audio (OGG/MP3)",
    language: "Instrumental",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/audio/Whistle MOP.ogg",
    poster: "/images/memorial-candles.png",
    downloadUrl: "/media/audio/Whistle MOP.ogg",
    fileSize: "3.2 MB",
    featured: true,
    isAudio: true,
    description: {
      en: "The original commemorative audio piece combining traditional coastal woodwind melodies with ambient orchestration dedicated to the 120 children of Minab.",
      fa: "قطعه موسیقی اختصاصی یادبود که با تلفیق نوای نی‌انبان و ملودی‌های ساحلی جنوب ایران در گرامیداشت کودکان معصوم میناب ساخته شده است."
    },
    tags: ["Soundtrack", "Melody of Peace", "PFP Official", "Audio Score"]
  },

  // ==========================================
  // 7. VISUAL MEMORIALS & MOSAIC ASSETS
  // ==========================================
  {
    id: "100-faces-of-peace-mosaic",
    slug: "100-faces-of-peace-animated-mosaic",
    category: "visual_memorials",
    categoryLabel: { en: "Visual Memorial", fa: "یادبود تصویری" },
    title: {
      en: "100 Faces of Peace: Animated Memorial Mosaic",
      fa: "موزاییک متحرک «۱۰۰ چهره صلح»: یادبود کودکان میناب"
    },
    producer: "People for Peace Creative Studio",
    runtime: "Seamless Loop",
    resolution: "Animated Graphic (GIF/WebP)",
    language: "Visual",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/visuals/100_faces_of_peace.gif",
    poster: "/images/og-memorial.png",
    downloadUrl: "/media/visuals/100_faces_of_peace.gif",
    fileSize: "23.0 MB",
    featured: true,
    isImage: true,
    description: {
      en: "A continuous animated tribute cycling through the verified portraits and identities of 100 students killed in the Shajareh Tayyebeh tragedy.",
      fa: "طراحی متحرک و پیوسته از تصاویر و چهره‌های احراز هویت شده ۱۰۰ دانش‌آموز شهید دبستان شجره طیبه میناب."
    },
    tags: ["100 Faces", "Memorial Mosaic", "PFP Visuals", "Children of Minab"]
  },
  {
    id: "eyes-that-ask-looped-visual",
    slug: "eyes-that-ask-projection-visual",
    category: "visual_memorials",
    categoryLabel: { en: "Visual Memorial", fa: "یادبود تصویری" },
    title: {
      en: "Eyes That Ask: Projection Visual for Memorial Screenings",
      fa: "چشم‌هایی که می‌پرسند: اثر بصری ویژه اکران‌های یادبود"
    },
    producer: "People for Peace Creative Studio",
    runtime: "Seamless Loop",
    resolution: "High-Res Animated Graphic",
    language: "Visual",
    subtitles: ["English", "فارسی", "Suomi"],
    year: "2026",
    videoUrl: "/media/visuals/eyes_that_ask.gif",
    poster: "/images/memorial-bg.png",
    downloadUrl: "/media/visuals/eyes_that_ask.gif",
    fileSize: "14.0 MB",
    featured: false,
    isImage: true,
    description: {
      en: "A solemn, contemplative projection visual designed for public screenings, candlelit vigils, and international memorial events.",
      fa: "اثر تصویری طراحی‌شده جهت پخش در سالن‌های اکران، مراسم شمع‌افروزی و یادبودهای بین‌المللی در اروپا."
    },
    tags: ["Projection", "Eyes That Ask", "Memorial Vigils"]
  },

  // ==========================================
  // 8. MINAB SCHOOL & EYEWITNESS RAW ARCHIVE (36 ITEMS)
  // ==========================================
  {
      "id": "minab-eyewitness-01",
      "slug": "minab-eyewitness-01",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Alphabet Lesson & Young Mahan's Mother's Day Greeting ('I Love You, Beautiful Mother')",
          "fa": "تدریس نشانه «آ» و پیام کودکانه ماهان برای روز مادر («دوستت دارم مادر قشنگم»)"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:25",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_01_1406522.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_01_1406522.jpg",
      "fileSize": "2.5 MB",
      "featured": false,
      "description": {
          "en": "Ground-floor sky-blue classroom recording featuring raw, unedited audio of young student Mahan holding his handmade craft and telling his mother: 'Hello my beautiful mother, happy Mother's Day, I love you — from your son Mahan.'",
          "fa": "فیلم کلاسی از تدریس نشانه «آ» در کلاس آبی‌رنگ پسران که در آن «ماهان» کوچک با صدای کودکانه و واقعی خود رو به دوربین می‌گوید: «سلام مادر قشنگم، امروز روزت مبارک باشه، دوستت دارم مادر قشنگم، از طرف پسرت ماهان.»"
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Raw Classroom Audio",
          "Mahan",
          "Mother's Day",
          "Boys School"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_01_1406522.mp4"
  },
  {
      "id": "minab-eyewitness-02",
      "slug": "minab-eyewitness-02",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Final First-Grade Classroom Photos Sent to Mothers Moments Before Impact",
          "fa": "آخرین تصاویر کلاس اول ابتدایی ارسالی معلم شهید در گروه مادران لحظاتی پیش از اصابت موشک"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:09",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_02_1406537.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_02_1406537.jpg",
      "fileSize": "0.5 MB",
      "featured": false,
      "description": {
          "en": "Photographs captured inside the first-grade girls' classroom by their teacher and shared in the mothers' group chat minutes before the February 28, 2026 strike.",
          "fa": "تصاویر ثبت‌شده توسط معلم شهید پایه اول ابتدایی از دانش‌آموزان دختر پشت نیمکت‌های سبز که دقایقی پیش از حمله موشکی ۹ اسفند ۱۴۰۴ در گروه مادران ارسال شده بود."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "First Grade",
          "Pre-Strike Classroom",
          "Final Moments",
          "Girls School"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_02_1406537.mp4"
  },
  {
      "id": "minab-eyewitness-03",
      "slug": "minab-eyewitness-03",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "The Final Match — Schoolboys Playing Football on the Morning of February 28",
          "fa": "آخرین بازی — فوتبال دانش‌آموزان دبستان شجره طیبه در صبح روز حادثه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:46",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_03_1406521.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_03_1406521.jpg",
      "fileSize": "5.5 MB",
      "featured": false,
      "description": {
          "en": "Footage recorded on the sports pitch beside Shajareh Tayyebeh School showing boys playing football on the morning of the February 28, 2026 attack.",
          "fa": "تصاویر ثبت‌شده از آخرین بازی فوتبال دانش‌آموزان پسر دبستان شجره طیبه میناب در زمین ورزشی مدرسه پیش از وقوع حمله."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Football Pitch",
          "Day of Strike",
          "Boys School"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_03_1406521.mp4"
  },
  {
      "id": "minab-eyewitness-04",
      "slug": "minab-eyewitness-04",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Unedited Classroom Laughter — Boys Playing Science Game at Green Desks",
          "fa": "خنده‌های بی‌وقفه کودکانه در کلاس درس پسران پشت نیمکت‌های سبز (صدای طبیعی)"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:35",
      "resolution": "720×720",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_04_1406525.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_04_1406525.jpg",
      "fileSize": "7.4 MB",
      "featured": false,
      "description": {
          "en": "Raw, unedited classroom recording with natural audio: Shajareh Tayyebeh schoolboys at lime-green desks burst into joyful laughter during a playful classroom activity with their teacher.",
          "fa": "فیلم خام با صدای کاملاً طبیعی و بدون موسیقی از شوخی و خنده‌های کودکانه دانش‌آموزان پسر پشت نیمکت‌های سبز کلاس درس به همراه آموزگارشان."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Raw Classroom Audio",
          "Boys School",
          "Living Memory"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_04_1406525.mp4"
  },
  {
      "id": "minab-eyewitness-05",
      "slug": "minab-eyewitness-05",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "On-Site Spatial Testimony at the Sheared Central Staircase (Raw Field Audio)",
          "fa": "روایت میدانی در برابر راه‌پله مرکزی منهدم‌شده از تفکیک طبقات و اصابت دو موشک"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:38",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_05_1406505.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_05_1406505.jpg",
      "fileSize": "13.1 MB",
      "featured": false,
      "description": {
          "en": "Unedited 38-second field walkthrough with clear Persian narration standing directly before the sheared central stairwell, confirming the girls' upper floor, boys' ground floor, central staircase impact point, and the second strike on gathered families.",
          "fa": "گزارش میدانی ۳۸ ثانیه‌ای با صدای مستقیم از مقابل راه‌پله فروریخته مرکزی که چیدمان طبقه بالای دختران، طبقه همکف پسران، محل اصابت موشک اول به راه‌پله و اصابت موشک دوم به تجمع خانواده‌ها را نشان می‌دهد."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Spatial Verification",
          "Central Staircase",
          "Double-Tap",
          "Raw Eyewitness Audio"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_05_1406505.mp4"
  },
  {
      "id": "minab-eyewitness-06",
      "slug": "minab-eyewitness-06",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Raw Courtyard Phone Video Minutes After Impact — Torn Pages & Cries for Classmates",
          "fa": "فیلم خام تلفن همراه در حیاط پر از دود دبستان دقایقی پس از اصابت موشک"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:17",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_06_1406519.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_06_1406519.jpg",
      "fileSize": "15.8 MB",
      "featured": false,
      "description": {
          "en": "Unedited citizen phone video with raw on-site audio recorded inside the dust-choked schoolyard minutes after the strike: torn homework sheets cover the ground while families rush toward the smoking ruins calling out names.",
          "fa": "ویدیوی خام شهروندی با صدای طبیعی صحنه در دقایق نخست پس از حمله؛ برگه‌های پراکنده دفتر مشق روی خاک حیاط، دود سیاه و فریاد خانواده‌ها در جستجوی کودکان."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "First Minutes",
          "Raw Eyewitness Audio",
          "Courtyard",
          "Primary Evidence"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_06_1406519.mp4"
  },
  {
      "id": "minab-eyewitness-07",
      "slug": "minab-eyewitness-07",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Before & After the Strike — Shajareh Tayyebeh Playroom & Ball-Pit",
          "fa": "خانه بازی دبستان شجره طیبه — مقایسه پیش از انفجار و پس از فروریختن سقف"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:37",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_07_1406523.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_07_1406523.jpg",
      "fileSize": "5.5 MB",
      "featured": false,
      "description": {
          "en": "Direct visual comparison showing preschool and primary children jumping happily in the school's mural-painted playroom and ball-pit before February 28, followed by the exact same painted wall buried beneath collapsed roof beams.",
          "fa": "مقایسه تکان‌دهنده از شادی کودکان در «خانه بازی» رنگارنگ دبستان شجره طیبه پیش از حمله و ویرانه همان اتاق با نقاشی‌های دیواری در زیر تیرآهن و آوار پس از انفجار."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Before & After",
          "Playroom",
          "Spatial Verification"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_07_1406523.mp4"
  },
  {
      "id": "minab-eyewitness-08",
      "slug": "minab-eyewitness-08",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Pink-Door Classroom Group Photo Under Rainbow Balloons — Only Four Children Survived",
          "fa": "عکس دسته‌جمعی دانش‌آموزان در کلاس درِ صورتی — تنها ۴ کودک از این جمع زنده ماندند"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "800×450",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_08_1406490.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_08_1406490.jpg",
      "fileSize": "0.1 MB",
      "featured": false,
      "description": {
          "en": "Pre-strike group photograph of fourteen young schoolgirls and their teacher standing beneath rainbow balloons inside a classroom with pink doors; eyewitness family records confirm only four children in this photograph survived the February 28 strike.",
          "fa": "عکس یادگاری چهارده دانش‌آموز دختر و معلمشان زیر بادکنک‌های رنگی در کلاس با درهای صورتی؛ به گواهی خانواده‌ها تنها ۴ نفر از کودکان حاضر در این عکس از حمله موشکی زنده ماندند."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Class Photo",
          "Survivors & Martyrs",
          "Girls School",
          "Primary Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-09",
      "slug": "minab-eyewitness-09",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Aerial Drone Footage — Over One Hundred Graves Prepared Side by Side & Mass Funeral",
          "fa": "تصویر هوایی تکان‌دهنده از حفر صدها مزار کوچک در کنار هم و تشییع پیکر کودکان میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:38",
      "resolution": "716×1274",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_09_1406491.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_09_1406491.jpg",
      "fileSize": "10.4 MB",
      "featured": false,
      "description": {
          "en": "Overhead drone video documenting two long rows of freshly excavated graves prepared side by side for the schoolchildren and educators of Shajareh Tayyebeh, followed by thousands of mourners gathering around them.",
          "fa": "ویدیوی هوایی از ردیف‌های طولانی مزارهای کوچک آماده‌شده در کنار یکدیگر برای دانش‌آموزان و معلمان دبستان شجره طیبه و حضور هزاران نفر از مردم سوگوار در مراسم خاکسپاری."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Aerial Footage",
          "Mass Funeral",
          "Cemetery",
          "Primary Scale Evidence"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_09_1406491.mp4"
  },
  {
      "id": "minab-eyewitness-10",
      "slug": "minab-eyewitness-10",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Young Surviving Sisters Reyhaneh & Mastaneh Looking Back at Their Burning School",
          "fa": "نگاه بهت‌زده «ریحانه» و «مستانه» در میان گردوغبار به ویرانه مدرسه‌شان"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:06",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_10_1406506.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_10_1406506.jpg",
      "fileSize": "0.7 MB",
      "featured": false,
      "description": {
          "en": "Raw eyewitness phone clip capturing two tiny surviving schoolgirls, Reyhaneh and Mastaneh, covered in grey blast dust as crowds run toward the smoking school behind them.",
          "fa": "فیلم خام لحظات نخست پس از انفجار از دو دانش‌آموز خردسال بازمانده، «ریحانه» و «مستانه»، با چهره‌های خاک‌آلود در برابر دود و ویرانه مدرسه‌شان."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Child Survivors",
          "First Minutes",
          "Raw Eyewitness Audio"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_10_1406506.mp4"
  },
  {
      "id": "minab-eyewitness-11",
      "slug": "minab-eyewitness-11",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Rows of Recovered Children's Shoes, Backpacks & Homework Laid Out on Carpets",
          "fa": "ردیف کفش‌های کوچک، کیف‌ها و دفترهای مشق کودکان بر روی فرش برای شناسایی"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:10",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_11_1406509.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_11_1406509.jpg",
      "fileSize": "2.4 MB",
      "featured": false,
      "description": {
          "en": "Heartbreaking interior documentation showing dozens of small dusty school shoes, pastel backpacks, and open homework notebooks arranged in rows on carpets so families could identify their children.",
          "fa": "تصاویری تکان‌دهنده از ده‌ها جفت کفش کوچک خاکی، کوله‌پشتی و کتاب‌های درسی به‌جامانده از دانش‌آموزان که برای شناسایی توسط والدین کنار هم چیده شده‌اند."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Recovered Belongings",
          "Children's Shoes",
          "Aftermath"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_11_1406509.mp4"
  },
  {
      "id": "minab-eyewitness-12",
      "slug": "minab-eyewitness-12",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Recovering a Child's 'MY HEART' Backpack & Torn Notebooks from Rubble",
          "fa": "بیرون کشیدن کوله‌پشتی «MY HEART» و دفترهای مشق کودک از زیر آوار"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:28",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_12_1406534.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_12_1406534.jpg",
      "fileSize": "5.6 MB",
      "featured": false,
      "description": {
          "en": "On-site footage of rescuers lifting a dust-covered school backpack stamped 'MY HEART' and shrapnel-torn homework notebooks from the collapsed classroom slabs.",
          "fa": "تصاویر میدانی از بیرون آوردن کیف مدرسه خاک‌گرفته یک کودک با نوشته MY HEART و کتاب و دفترهای پاره‌شده از میان آوار کلاس‌های درس."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Schoolbags",
          "Rubble Recovery",
          "Physical Evidence",
          "Aftermath"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_12_1406534.mp4"
  },
  {
      "id": "minab-eyewitness-13",
      "slug": "minab-eyewitness-13",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Child's Dust-Covered Sneaker Lifted from Crushed Classroom Concrete",
          "fa": "بیرون آوردن کفش کوچک خاک‌گرفته دانش‌آموز از میان بتن و آوار کلاس"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:46",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_13_1406532.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_13_1406532.jpg",
      "fileSize": "17.6 MB",
      "featured": false,
      "description": {
          "en": "Close-up on-site documentation of gloved rescue workers uncovering a small grey sneaker buried among shattered concrete blocks of the school.",
          "fa": "نمای نزدیک از دستان امدادگران هنگام بیرون آوردن یک لنگه کفش کوچک خاک‌گرفته دانش‌آموز از لابه‌لای سنگ و بتن کلاس‌های فروریخته."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Recovered Belongings",
          "Child's Shoe",
          "Rubble Forensics"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_13_1406532.mp4"
  },
  {
      "id": "minab-eyewitness-14",
      "slug": "minab-eyewitness-14",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Bereaved Mothers Sitting Atop the Collapsed Classroom Rubble Mound",
          "fa": "مادران سیاه‌پوش نشسته بر تل آوار کلاس‌های فروریخته در جستجوی فرزندان"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:14",
      "resolution": "1280×720",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_14_1406504.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_14_1406504.jpg",
      "fileSize": "5.0 MB",
      "featured": false,
      "description": {
          "en": "Wide 16:9 field recording showing black-clad Minab mothers sitting directly on the mound of crushed concrete where the classrooms stood, digging through stones with their bare hands.",
          "fa": "نمای افقی از مادران داغدار میناب که بر روی تپه‌ای از بتن و آوار کلاس‌های درس نشسته و با دست خالی خاک‌ها را کنار می‌زنند."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Mothers of Minab",
          "Aftermath",
          "Rubble"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_14_1406504.mp4"
  },
  {
      "id": "minab-eyewitness-15",
      "slug": "minab-eyewitness-15",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Pre-Strike Walkthrough of Intact Classrooms, Pink Doors, Gate & Prayer Room",
          "fa": "تصاویر پیش از حمله از درهای صورتی کلاس‌ها، حیاط، نمازخانه و سردر دبستان دخترانه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:25",
      "resolution": "964×720",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_15_1406530.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_15_1406530.jpg",
      "fileSize": "2.3 MB",
      "featured": false,
      "description": {
          "en": "Archival video showing the intact architecture of Shajareh Tayyebeh Girls' Primary School: pink classroom doors with paper flowers, painted courtyard murals, school gate signage, and carpeted prayer hall.",
          "fa": "گزارش تصویری پیش از حادثه از فضای داخلی و بیرونی دبستان دخترانه شجره طیبه شامل درهای صورتی کلاس‌ها، نقاشی‌های حیاط، تابلوی سردر و نمازخانه مدرسه."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Spatial Verification",
          "School Architecture",
          "Pre-Strike"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_15_1406530.mp4"
  },
  {
      "id": "minab-eyewitness-16",
      "slug": "minab-eyewitness-16",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "First-Grade Water Festival — Girls in Blue Paper Crowns Inside Pink-Door Room",
          "fa": "جشن آب پایه اول — هم‌خوانی دختران با تاج‌های کاغذی آبی در کلاس درِ صورتی"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:26",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_16_1406524.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_16_1406524.jpg",
      "fileSize": "7.2 MB",
      "featured": false,
      "description": {
          "en": "Pre-strike classroom recording of first-grade girls seated on blue chairs wearing handmade water-drop paper crowns inside a classroom with pink doors.",
          "fa": "فیلم آرشیوی از جشن کلاسی دانش‌آموزان دختر کلاس اول با کاردستی قطره‌های آب در اتاقی با درهای صورتی در دبستان شجره طیبه."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "First Grade",
          "Girls School",
          "Spatial Verification"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_16_1406524.mp4"
  },
  {
      "id": "minab-eyewitness-17",
      "slug": "minab-eyewitness-17",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Schoolgirls Waving Flags in the Sunny Courtyard Beside Wall Murals",
          "fa": "صف صبحگاهی و لبخند دختران دانش‌آموز در حیاط دبستان کنار نقاشی‌های دیواری"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:26",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_17_1406528.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_17_1406528.jpg",
      "fileSize": "6.3 MB",
      "featured": false,
      "description": {
          "en": "Pre-strike school archive footage walking along a line of smiling Shajareh Tayyebeh schoolgirls waving small flags in the courtyard.",
          "fa": "فیلم آرشیوی مدرسه از صف پرشور و لبخند دانش‌آموزان دختر در حیاط دبستان شجره طیبه در کنار نقاشی‌های کودکانه دیوار."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Courtyard",
          "Morning Assembly",
          "Girls School"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_17_1406528.mp4"
  },
  {
      "id": "minab-eyewitness-18",
      "slug": "minab-eyewitness-18",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "The Final Field Trip — Shajareh Tayyebeh Schoolboys' Excursion",
          "fa": "آخرین اردوی دانش‌آموزان پسر دبستان شجره طیبه میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "2:20",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_18_1406533.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_18_1406533.jpg",
      "fileSize": "23.1 MB",
      "featured": false,
      "description": {
          "en": "Two-minute archival recording of Shajareh Tayyebeh schoolboys laughing, riding the school bus, and visiting a local greenhouse on their final school excursion before February 28, 2026 (shared with families' permission).",
          "fa": "فیلم یادگاری دو دقیقه‌ای از آخرین اردوی تفریحی دانش‌آموزان پسر دبستان شجره طیبه میناب در اتوبوس و گلخانه پیش از فاجعه ۹ اسفند (منتشرشده با اجازه خانواده‌های شهدا)."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "School Excursion",
          "Boys School",
          "Pre-Strike Life"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_18_1406533.mp4"
  },
  {
      "id": "minab-eyewitness-19",
      "slug": "minab-eyewitness-19",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "First Responders & Residents Climbing Smoking Classroom Rubble",
          "fa": "تلاش شهروندان با دست خالی بر فراز آوار در حال سوختن کلاس‌ها در دقایق نخست"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:08",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_19_1406518.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_19_1406518.jpg",
      "fileSize": "6.9 MB",
      "featured": false,
      "description": {
          "en": "Raw citizen phone clip with unedited audio showing local residents climbing onto the fractured concrete slabs immediately after the strike while black smoke rises behind them.",
          "fa": "فیلم خام مردمی از حضور شتابان اهالی میناب بر روی تخته‌سنگ‌های فروریخته مدرسه در دقایق اولیه پس از انفجار."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "First Minutes",
          "Rescue Efforts",
          "Raw Eyewitness Audio"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_19_1406518.mp4"
  },
  {
      "id": "minab-eyewitness-20",
      "slug": "minab-eyewitness-20",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Mother Clutching Recovered Schoolbooks Beside Collapsed Concrete Slabs",
          "fa": "مادر داغدار با کتاب‌های درسی فرزندش در آغوش بر روی آوار مدرسه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:22",
      "resolution": "480×854",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_20_1406508.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_20_1406508.jpg",
      "fileSize": "2.7 MB",
      "featured": false,
      "description": {
          "en": "On-site video of a black-clad mother standing among broken concrete beams clutching recovered schoolbooks and folders while crowds search the upper rubble.",
          "fa": "حضور مادر داغدار در میان ستون‌ها و سقف فروریخته دبستان در حالی که کتاب‌ها و پوشه‌های پیداشده از زیر آوار را در آغوش گرفته است."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Mothers of Minab",
          "Rubble Search",
          "Aftermath"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_20_1406508.mp4"
  },
  {
      "id": "minab-eyewitness-21",
      "slug": "minab-eyewitness-21",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Sifting Classroom Rubble by Hand in Search of Remains & Shrapnel",
          "fa": "جستجوی وجب‌به‌وجب خاک و آوار مدرسه با دست توسط خانواده‌ها و امدادگران"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:35",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_21_1406507.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_21_1406507.jpg",
      "fileSize": "6.6 MB",
      "featured": false,
      "description": {
          "en": "Close-up field footage of volunteers and bereaved relatives carefully sifting fine rubble dust and metal shrapnel fragments inside the destroyed school compound.",
          "fa": "تصاویر نزدیک از جستجوی دقیق خاک، سنگ‌ریزه‌ها و ترکش‌ها در محل کلاس‌های تخریب‌شده دبستان شجره طیبه."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Rubble Forensics",
          "Shrapnel",
          "Aftermath"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_21_1406507.mp4"
  },
  {
      "id": "minab-eyewitness-22",
      "slug": "minab-eyewitness-22",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Portraits of Childhood — Martyred Schoolgirls on Bus Trip & in Class",
          "fa": "قاب‌های کودکی — تصاویر یادگاری دختران شهید در اردو و کلاس درس"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:42",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_22_1406529.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_22_1406529.jpg",
      "fileSize": "5.4 MB",
      "featured": false,
      "description": {
          "en": "Archival photographs and clips of young Shajareh Tayyebeh schoolgirls smiling with storybooks, backpacks, and classmates prior to the attack.",
          "fa": "مجموعه تصاویر و لحظات به‌جامانده از دانش‌آموزان دختر دبستان شجره طیبه در اردوی دانش‌آموزی و پشت نیمکت‌های کلاس."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Girls School",
          "Student Portraits",
          "Memorial"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_22_1406529.mp4"
  },
  {
      "id": "minab-eyewitness-23",
      "slug": "minab-eyewitness-23",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Schoolgirls Playing Clapping Games During Courtyard Recess",
          "fa": "بازی و شادی دختران دانش‌آموز در زنگ تفریح حیاط مدرسه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:18",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_23_1406531.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_23_1406531.jpg",
      "fileSize": "1.3 MB",
      "featured": false,
      "description": {
          "en": "Pre-strike clip of Shajareh Tayyebeh schoolgirls in green uniforms and white headscarves playing hand-clapping games together in the schoolyard.",
          "fa": "تصویری از زنگ تفریح و بازی کودکانه دانش‌آموزان دختر دبستان شجره طیبه در حیاط مدرسه پیش از حمله."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Girls School",
          "Recess",
          "Pre-Strike Life"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_23_1406531.mp4"
  },
  {
      "id": "minab-eyewitness-24",
      "slug": "minab-eyewitness-24",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Young Student's Birthday Smile & Memorial Portrait",
          "fa": "لبخند جشن تولد دانش‌آموز شهید دبستان میناب و قاب یادبود او"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:13",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_24_1406535.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_24_1406535.jpg",
      "fileSize": "3.0 MB",
      "featured": false,
      "description": {
          "en": "Archive clip contrasting a young Shajareh Tayyebeh schoolboy blowing out candles on a football birthday cake with his framed memorial portrait.",
          "fa": "ویدیوی کوتاهی از شادی کودکانه یکی از دانش‌آموزان پسر دبستان میناب در جشن تولدش در کنار قاب تصویر یادبود او پس از شهادت."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Student Tribute",
          "Pre-Strike Life",
          "Memorial"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_24_1406535.mp4"
  },
  {
      "id": "minab-eyewitness-25",
      "slug": "minab-eyewitness-25",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Wide View of the Sheared Two-Story School Facade Draped in Mourning Cloth",
          "fa": "نمای کامل برش دوطبقه ساختمان منهدم‌شده دبستان شجره طیبه میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "0:26",
      "resolution": "720×1280",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_25_1406520.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_25_1406520.jpg",
      "fileSize": "3.5 MB",
      "featured": false,
      "description": {
          "en": "Wide exterior recording of the bombed two-story school building showing the complete collapse of the central hall and western classrooms.",
          "fa": "نمای باز از ساختمان دوطبقه آسیب‌دیده دبستان شجره طیبه که وسعت تخریب سالن میانی و کلاس‌ها را نشان می‌دهد."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Structural Damage",
          "Aftermath",
          "Spatial Verification"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_25_1406520.mp4"
  },
  {
      "id": "minab-eyewitness-26",
      "slug": "minab-eyewitness-26",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Archival Montage of Shajareh Tayyebeh Schoolgirls in Courtyard & Corridors",
          "fa": "مجموعه تصاویر آرشیوی دانش‌آموزان دختر در حیاط و راهروهای دبستان میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "1:25",
      "resolution": "592×1052",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_26_1406526.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_26_1406526.jpg",
      "fileSize": "6.2 MB",
      "featured": false,
      "description": {
          "en": "Extended compilation of pre-strike school clips showing girls gathered in the sunny courtyard, beside murals, and on the morning assembly lines.",
          "fa": "مجموعه‌ای از ویدیوهای کوتاه آرشیوی پیش از حمله از حضور و هم‌خوانی دانش‌آموزان دختر در حیاط و خط‌کشی صف صبحگاهی دبستان."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Girls School",
          "Courtyard",
          "School Archive"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_26_1406526.mp4"
  },
  {
      "id": "minab-eyewitness-27",
      "slug": "minab-eyewitness-27",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Bereaved Minab Mothers & Fathers Holding Portraits in Collective Mourning",
          "fa": "سوگواری مادران و پدران داغدار مینابی با قاب‌عکس فرزندان در دست"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "1:24",
      "resolution": "1276×720",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_27_1406527.mp4",
      "poster": "/media/raw_eyewitness/posters/minab_ew_27_1406527.jpg",
      "fileSize": "11.8 MB",
      "featured": false,
      "description": {
          "en": "Documentary footage of grieving mothers and fathers in Minab embracing and holding framed portraits of their schoolchildren.",
          "fa": "تصاویری از گردهمایی سوگواری خانواده‌ها، پدران و مادران داغدار میناب در حالی که قاب‌عکس کودکان شهیدشان را در آغوش گرفته‌اند."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Bereaved Families",
          "Mothers of Minab",
          "Memorial"
      ],
      "videoUrl": "/media/raw_eyewitness/minab_ew_27_1406527.mp4"
  },
  {
      "id": "minab-eyewitness-28",
      "slug": "minab-eyewitness-28",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Lone Mother Sitting in Candlelight Before the Sheared Two-Story Ruins",
          "fa": "مادری تنها در برابر شکاف دوطبقه ساختمان ویران‌شده دبستان در شب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_28_1406493.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_28_1406493.jpg",
      "fileSize": "0.2 MB",
      "featured": false,
      "description": {
          "en": "Striking night photograph of a single black-clad woman sitting quietly with a candle at the foot of the sheared two-story central stairwell of Shajareh Tayyebeh School.",
          "fa": "عکسی تکان‌دهنده از نشستن خاموش یک مادر سیاه‌پوش با شمعی روشن در پای شکاف عظیم دوطبقه دبستان شجره طیبه در شب."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Mothers of Minab",
          "Night Vigil",
          "Central Staircase"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-29",
      "slug": "minab-eyewitness-29",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Wall of Eyes — Street Memorial Mural of the Minab Schoolchildren",
          "fa": "دیوارنگاره «چشمان منتظر» — نگاه کودکان شهید دبستان میناب بر دیوار شهر"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_29_1406495.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_29_1406495.jpg",
      "fileSize": "0.2 MB",
      "featured": false,
      "description": {
          "en": "Photograph of a long exterior perimeter wall lined with close-up photographic panels of the eyes of the martyred Minab schoolchildren.",
          "fa": "تصویر دیوارنگاره یادبود در میناب که چشمان معصوم کودکان شهید دبستان شجره طیبه را در قاب‌های پیاپی به تصویر کشیده است."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Eyes Memorial",
          "Public Mural",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-30",
      "slug": "minab-eyewitness-30",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "'THEIR BLOOD DEMANDS JUSTICE, NOT SILENCE' — Vigil Placard at the Bombed School",
          "fa": "پلاکارد «خون آنان عدالت می‌طلبد، نه سکوت» در کنار ویرانه سرخ‌فام دبستان"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_30_1406497.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_30_1406497.jpg",
      "fileSize": "0.1 MB",
      "featured": false,
      "description": {
          "en": "Photograph taken at the illuminated ruins of Shajareh Tayyebeh School featuring a handwritten English placard reading 'THEIR BLOOD DEMANDS JUSTICE, NOT SILENCE' beside portraits on the rubble.",
          "fa": "تصویری از محل ویرانه‌های نورپردازی‌شده دبستان شجره طیبه با دست‌نوشته انگلیسی «خون آنان عدالت می‌طلبد، نه سکوت» در کنار قاب‌عکس کودکان."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Accountability",
          "Justice Vigil",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-31",
      "slug": "minab-eyewitness-31",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Framed Portraits of Martyred Children Placed Atop Broken Classroom Concrete",
          "fa": "قاب‌عکس‌های کودکان شهید بر روی تکه‌سنگ‌ها و آوار کلاس‌های درس"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_31_1406498.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_31_1406498.jpg",
      "fileSize": "0.3 MB",
      "featured": false,
      "description": {
          "en": "Close-up photograph of framed portraits of martyred Shajareh Tayyebeh schoolgirls and schoolboys resting on shattered concrete slabs during a dusk vigil.",
          "fa": "نمای نزدیک از قاب‌عکس‌های دانش‌آموزان دختر و پسر شهید که در مراسم یادبود شبانه بر روی سنگ‌ها و آوار کلاس چیده شده است."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Vigil",
          "Student Portraits",
          "School Ruins"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-32",
      "slug": "minab-eyewitness-32",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Rows of Children's Graves & Portraits in the Minab Martyrs' Cemetery",
          "fa": "ردیف مزارهای کودکان دانش‌آموز با قاب‌عکس‌هایشان در گلزار شهدای میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_32_1406492.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_32_1406492.jpg",
      "fileSize": "0.3 MB",
      "featured": false,
      "description": {
          "en": "Photograph showing parallel rows of white graves for the schoolchildren of Shajareh Tayyebeh, each marked with the child's portrait.",
          "fa": "تصویری از ردیف‌های به‌هم‌پیوسته مزار دانش‌آموزان شهید دبستان شجره طیبه میناب با قاب‌عکس‌های کودکان بر هر مزار."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Cemetery",
          "Memorial",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-33",
      "slug": "minab-eyewitness-33",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Dusk Photograph of the Collapsed Western Wing & Twisted Rebar",
          "fa": "نمای شامگاهی از بال غربی فروریخته و میلگردهای درهم‌پیچیده دبستان"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_33_1406494.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_33_1406494.jpg",
      "fileSize": "0.2 MB",
      "featured": false,
      "description": {
          "en": "Wide dusk photograph showing the red-lit interior void of the sheared school building and tangled steel reinforcement bars in the foreground.",
          "fa": "نمای باز شامگاهی از بخش فروریخته ساختمان مدرسه و انبوه بتن و میلگردهای متلاشی‌شده در پیش‌زمینه."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Structural Damage",
          "Dusk Vigil",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-34",
      "slug": "minab-eyewitness-34",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Memorial Banner of All Martyred Students & Teachers Draped Over School Ruins",
          "fa": "بنر بزرگ تصاویر شهدای دانش‌آموز و معلم بر نمای باقی‌مانده دبستان شجره طیبه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×811",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_34_1406499.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_34_1406499.jpg",
      "fileSize": "0.1 MB",
      "featured": false,
      "description": {
          "en": "Daylight photograph of the surviving eastern wing of Shajareh Tayyebeh School draped with a giant banner bearing the portraits of the martyred children and educators.",
          "fa": "تصویر روز از ساختمان نیمه‌ویران دبستان شجره طیبه که بنر بزرگی از چهره دانش‌آموزان و آموزگاران شهید بر آن آویخته شده است."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Memorial Banner",
          "School Ruins",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-35",
      "slug": "minab-eyewitness-35",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Roadside Sign Marking the Site of the Shajareh Tayyebeh School Massacre",
          "fa": "تابلوی راهنمای محل شهادت دانش‌آموزان دبستان شجره طیبه در میناب"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "1080×810",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_35_1406496.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_35_1406496.jpg",
      "fileSize": "0.2 MB",
      "featured": false,
      "description": {
          "en": "Photograph of the public roadside sign in Minab directing visitors and mourners to the site of the Shajareh Tayyebeh Primary School strike.",
          "fa": "تصویر تابلوی «مقتل شهدای مدرسه شجره طیبه میناب» در مسیر منتهی به ساختمان مدرسه."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Minab",
          "Site Documentation",
          "Photo Evidence"
      ],
      "isImage": true
  },
  {
      "id": "minab-eyewitness-36",
      "slug": "minab-eyewitness-36",
      "category": "eyewitness",
      "categoryLabel": {
          "en": "Eyewitness & School Archive",
          "fa": "آرشیو مدرسه و روایت شاهدان"
      },
      "title": {
          "en": "Classroom Whiteboard Portrait — 'Hope & Iran'",
          "fa": "تصویر یادگاری پای تخته کلاس درس دبستان شجره طیبه"
      },
      "producer": "Minab School & Eyewitness Archive",
      "runtime": "Photo",
      "resolution": "689×534",
      "language": "Farsi",
      "year": "2026",
      "downloadUrl": "/media/raw_eyewitness/minab_ew_36_1406536.jpg",
      "poster": "/media/raw_eyewitness/minab_ew_36_1406536.jpg",
      "fileSize": "0.1 MB",
      "featured": false,
      "description": {
          "en": "Pre-strike classroom photograph of a young Shajareh Tayyebeh schoolboy and his mother/educator beside the Persian alphabet lesson on the whiteboard.",
          "fa": "تصویر یادگاری پیش از حمله از دانش‌آموز خردسال در کنار تخته سفید کلاس درس دبستان شجره طیبه میناب."
      },
      "tags": [
          "Eyewitness Archive",
          "Minab School",
          "Classroom Photo",
          "Boys School",
          "Pre-Strike"
      ],
      "isImage": true
  },
];

if (typeof module !== 'undefined' && module.exports) {
  module.exports = PFP_MEDIA_DATA;
}
