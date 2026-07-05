"""
Management command to seed/restore campaign and task data.

Recreates the Justice for Minab Children campaign with tasks
aligned to the JusticeForMinab action plan, with trilingual support (EN/FA/AR).

Usage:
    python manage.py seed_campaign_data
    python manage.py seed_campaign_data --force  # Overwrite existing data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.campaigns.models import Campaign
from apps.tasks.models import Task, KeyTweet

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed campaign and task data for Justice for Minab Children'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete existing campaigns/tasks before seeding',
        )

    def handle(self, *args, **options):
        if options['force']:
            self.stdout.write('Deleting existing data...')
            KeyTweet.objects.all().delete()
            Task.objects.all().delete()
            Campaign.objects.all().delete()

        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        if not admin_user:
            self.stderr.write(self.style.ERROR('No users found. Create a user first.'))
            return

        self.stdout.write(f'Using admin user: {admin_user.username} (ID={admin_user.id})')

        # ─── Campaign: Justice for Minab Children ────────────────────
        campaign, created = Campaign.objects.get_or_create(
            name='Justice for Minab Children',
            defaults={
                'name_fa': 'عدالت برای کودکان میناب',
                'name_ar': 'العدالة لأطفال ميناب',
                'description': (
                    'Seeking justice and accountability for the 168 children killed '
                    'in the Minab school strike. On February 28, 2026, a devastating '
                    'strike on the Shajareh Tayyebeh girls\' elementary school killed '
                    'over 168 schoolgirls aged 7-12. We amplify their stories, demand '
                    'independent investigation through the ICC, and ensure the world '
                    'never forgets.'
                ),
                'short_description': 'Seeking justice for the 168 children of Minab 🕊️',
                'short_description_fa': 'جستجوی عدالت برای ۱۶۸ کودک میناب 🕊️',
                'short_description_ar': 'السعي لتحقيق العدالة لـ١٦٨ طفلاً من ميناب 🕊️',
                'campaign_type': 'hybrid',
                'status': 'active',
                'target_members': 1000,
                'target_activities': 5000,
                'target_twitter_posts': 2000,
                'twitter_hashtags': '#JusticeForMinab,#MinabSchoolMassacre,#168Children,#TrumpWarCrimes',
                'twitter_accounts': '@IntlCrimCourt,@UNHumanRights,@hrw,@amnesty,@SavetheChildren',
                'telegram_channel_id': -1003759398159,
                'created_by': admin_user,
            }
        )
        action = 'Created' if created else 'Already exists'
        self.stdout.write(self.style.SUCCESS(f'{action}: Campaign "{campaign.name}" (ID={campaign.id})'))

        # ─── Tasks (aligned with justiceForMinab action plan) ────────
        tasks_data = [
            {
                'task_type': 'twitter_post',
                'title': "Share a Child's Story",
                'title_fa': 'داستان یک کودک را به اشتراک بگذارید',
                'title_ar': 'شارك قصة طفل',
                'description': (
                    'Post a spotlight card with one child\'s name and photo. '
                    'Use their story to demand justice. Include '
                    '#JusticeForMinab and #168Children.'
                ),
                'description_fa': (
                    'یک کارت یادبود با نام و عکس یکی از کودکان پست کنید. '
                    'از داستان آنها برای مطالبه عدالت استفاده کنید.'
                ),
                'description_ar': (
                    'انشر بطاقة تذكارية باسم وصورة أحد الأطفال. '
                    'استخدم قصتهم للمطالبة بالعدالة.'
                ),
                'instructions': (
                    'Download a spotlight card from our content library, '
                    'share it on Twitter/X with the hashtags. Include '
                    'the child\'s name and age.'
                ),
                'instructions_fa': (
                    'یک کارت یادبود از کتابخانه محتوای ما دانلود کنید و '
                    'در توییتر/ایکس با هشتگ‌ها به اشتراک بگذارید.'
                ),
                'instructions_ar': (
                    'حمّل بطاقة تذكارية من مكتبة المحتوى وشاركها '
                    'على تويتر/إكس مع الوسوم.'
                ),
                'estimated_time': 5,
                'max_assignments': 500,
                'points': 15,
                'hashtags': '#JusticeForMinab,#168Children,#MinabSchoolMassacre',
                'mentions': '@IntlCrimCourt,@UNHumanRights,@hrw',
                'is_active': True,
            },
            {
                'task_type': 'twitter_comment',
                'title': 'Comment on Key Tweets',
                'title_fa': 'روی توییت‌های کلیدی نظر بگذارید',
                'title_ar': 'علّق على التغريدات الرئيسية',
                'description': (
                    'Reply to US officials and media posts with Minab facts. '
                    'Demand investigation and accountability.'
                ),
                'description_fa': (
                    'به پست‌های مقامات آمریکایی و رسانه‌ها با حقایق '
                    'میناب پاسخ دهید. خواستار تحقیق و پاسخگویی شوید.'
                ),
                'description_ar': (
                    'رد على منشورات المسؤولين الأمريكيين ووسائل الإعلام '
                    'بحقائق ميناب. طالب بالتحقيق والمساءلة.'
                ),
                'instructions': (
                    'Reply to key tweets from the ICC, UN Human Rights, HRW, '
                    'and other officials about Minab with respectful, factual '
                    'comments demanding investigation.'
                ),
                'instructions_fa': (
                    'به توییت‌های کلیدی دادگاه بین‌المللی، حقوق بشر سازمان ملل '
                    'و دیدبان حقوق بشر با نظرات محترمانه و واقعی پاسخ دهید.'
                ),
                'instructions_ar': (
                    'رد على التغريدات الرئيسية من المحكمة الجنائية الدولية '
                    'ومنظمات حقوق الإنسان بتعليقات محترمة وواقعية.'
                ),
                'estimated_time': 5,
                'max_assignments': 500,
                'points': 10,
                'is_active': True,
            },
            {
                'task_type': 'twitter_retweet',
                'title': 'Amplify Investigative Reports',
                'title_fa': 'گزارش‌های تحقیقی را تقویت کنید',
                'title_ar': 'عزّز التقارير الاستقصائية',
                'description': (
                    'Retweet NYT, BBC Verify, Washington Post reports on the '
                    'Minab strike. Amplify the facts.'
                ),
                'description_fa': (
                    'گزارش‌های NYT، BBC و واشنگتن پست درباره حمله به '
                    'میناب را ریتوییت کنید. حقایق را تقویت کنید.'
                ),
                'description_ar': (
                    'أعد تغريد تقارير NYT وBBC وواشنطن بوست عن '
                    'ضربة ميناب. عزّز الحقائق.'
                ),
                'instructions': (
                    'Search for investigative reports about the Minab school '
                    'strike from major media outlets and retweet them.'
                ),
                'instructions_fa': (
                    'گزارش‌های تحقیقی درباره حمله به دبستان میناب از '
                    'رسانه‌های بزرگ را جستجو و ریتوییت کنید.'
                ),
                'instructions_ar': (
                    'ابحث عن التقارير الاستقصائية عن ضربة مدرسة ميناب '
                    'من وسائل الإعلام الكبرى وأعد تغريدها.'
                ),
                'estimated_time': 3,
                'max_assignments': 500,
                'points': 5,
                'hashtags': '#JusticeForMinab,#MinabSchoolMassacre',
                'is_active': True,
            },
            {
                'task_type': 'content_creation',
                'title': 'Create Original Content for Minab',
                'title_fa': 'محتوای اصلی برای میناب بسازید',
                'title_ar': 'أنشئ محتوى أصلياً لميناب',
                'description': (
                    'Create your own video, art, poem, or thread about '
                    'the Minab children. Original content has the most impact.'
                ),
                'description_fa': (
                    'ویدیو، هنر، شعر یا رشته توییت خودتان درباره '
                    'کودکان میناب بسازید. محتوای اصلی بیشترین تأثیر را دارد.'
                ),
                'description_ar': (
                    'أنشئ فيديو أو فناً أو شعراً أو سلسلة تغريدات '
                    'عن أطفال ميناب. المحتوى الأصلي له أكبر تأثير.'
                ),
                'instructions': (
                    'Create and share original content about the children of '
                    'Minab. Use our content library for inspiration. Share on '
                    'Twitter/X with our campaign hashtags.'
                ),
                'instructions_fa': (
                    'محتوای اصلی درباره کودکان میناب بسازید و به اشتراک '
                    'بگذارید. از کتابخانه محتوای ما برای الهام استفاده کنید.'
                ),
                'instructions_ar': (
                    'أنشئ وشارك محتوى أصلياً عن أطفال ميناب. '
                    'استخدم مكتبة المحتوى للإلهام.'
                ),
                'estimated_time': 30,
                'max_assignments': 200,
                'points': 25,
                'is_active': True,
            },
            {
                'task_type': 'telegram_invite',
                'title': 'Grow the Movement',
                'title_fa': 'جنبش را رشد دهید',
                'title_ar': 'وسّع الحركة',
                'description': (
                    'Invite friends and family to join our Telegram bot. '
                    'Share the 100 Faces memorial video.'
                ),
                'description_fa': (
                    'دوستان و خانواده را به ربات تلگرام ما دعوت کنید. '
                    'ویدیوی یادبود ۱۰۰ چهره را به اشتراک بگذارید.'
                ),
                'description_ar': (
                    'ادعُ الأصدقاء والعائلة للانضمام إلى بوت تيليجرام. '
                    'شارك فيديو تذكار ١٠٠ وجه.'
                ),
                'instructions': (
                    'Share your personal invite link with friends, family, '
                    'and social media contacts. Each person who joins '
                    'strengthens our movement for justice.'
                ),
                'instructions_fa': (
                    'لینک دعوت شخصی خود را با دوستان، خانواده و '
                    'مخاطبان شبکه‌های اجتماعی به اشتراک بگذارید.'
                ),
                'instructions_ar': (
                    'شارك رابط الدعوة الشخصي مع الأصدقاء والعائلة '
                    'وجهات الاتصال على وسائل التواصل الاجتماعي.'
                ),
                'estimated_time': 5,
                'max_assignments': 1000,
                'points': 20,
                'is_active': True,
            },
        ]

        for td in tasks_data:
            points = td.pop('points')
            task, task_created = Task.objects.get_or_create(
                task_type=td['task_type'],
                campaign=campaign,
                defaults={
                    **td,
                    'created_by': admin_user,
                    'points': points,
                    'assignment_type': 'first_come',
                }
            )
            status = 'Created' if task_created else 'Exists'
            active = '✅' if task.is_active else '⏸️'
            self.stdout.write(f'  {active} {status}: {task.task_type} — {task.title} (ID={task.id})')

        # ─── KeyTweets for twitter_comment task ──────────────────────
        comment_task = Task.objects.filter(
            task_type='twitter_comment', campaign=campaign
        ).first()

        key_tweets_data = [
            {
                'author_name': 'International Criminal Court',
                'author_handle': '@IntlCrimCourt',
                'description': 'ICC statements on jurisdiction and war crimes investigation',
                'order': 1,
            },
            {
                'author_name': 'UN Human Rights',
                'author_handle': '@UNHumanRights',
                'description': 'UN Human Rights condemnation of civilian casualties in Minab',
                'order': 2,
            },
            {
                'author_name': 'Human Rights Watch',
                'author_handle': '@hrw',
                'description': 'HRW calls for the Minab school strike to be investigated as a war crime',
                'order': 3,
            },
            {
                'author_name': 'Amnesty International',
                'author_handle': '@amnesty',
                'description': 'Amnesty International documentation of the Minab attack',
                'order': 4,
            },
            {
                'author_name': 'Save the Children',
                'author_handle': '@SavetheChildren',
                'description': 'Save the Children coverage of children in conflict zones',
                'order': 5,
            },
        ]

        if comment_task:
            for ktd in key_tweets_data:
                tweet_url = (
                    f"https://x.com/{ktd['author_handle'].lstrip('@')}"
                    f"/status/placeholder_{ktd['order']}"
                )
                kt, kt_created = KeyTweet.objects.get_or_create(
                    task=comment_task,
                    author_handle=ktd['author_handle'],
                    defaults={
                        'tweet_url': tweet_url,
                        **ktd,
                    }
                )
                status = 'Created' if kt_created else 'Exists'
                self.stdout.write(f'    🔗 {status}: KT {kt.author_handle}')

        # ─── Summary ─────────────────────────────────────────────────
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write(self.style.SUCCESS(f'Campaign: {campaign.name} (ID={campaign.id})'))
        self.stdout.write(self.style.SUCCESS(
            f'Channel ID: {campaign.telegram_channel_id or "Not set"}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Total tasks: {Task.objects.filter(campaign=campaign).count()}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Active tasks: {Task.objects.filter(campaign=campaign, is_active=True).count()}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'KeyTweets: {KeyTweet.objects.filter(task__campaign=campaign).count()}'
        ))
        self.stdout.write(self.style.SUCCESS('═' * 50))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING(
            '⚠️  KeyTweet URLs are placeholders. Update with real tweet URLs via Django admin.'
        ))
        self.stdout.write(self.style.WARNING(
            '⚠️  Set telegram_group_id via Django admin when ready.'
        ))
