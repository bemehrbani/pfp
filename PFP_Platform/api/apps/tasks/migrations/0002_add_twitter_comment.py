# Generated manually for twitter_comment task type

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
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
                    ('research', 'Research'),
                    ('other', 'Other'),
                ],
                default='twitter_post',
                max_length=30,
            ),
        ),
    ]
