# Manually created migration for petition and mass_email task types

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_add_key_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(
                choices=[
                    ('twitter_post', 'Twitter Post'),
                    ('twitter_retweet', 'Twitter Retweet'),
                    ('twitter_comment', 'Twitter Comment'),
                    ('twitter_like', 'Twitter Like'),
                    ('telegram_share', 'Telegram Share'),
                    ('telegram_invite', 'Telegram Invite'),
                    ('content_creation', 'Content Creation'),
                    ('petition', 'Petition'),
                    ('mass_email', 'Mass Email'),
                    ('research', 'Research'),
                    ('other', 'Other'),
                ],
                default='twitter_post',
                max_length=30,
            ),
        ),
    ]
