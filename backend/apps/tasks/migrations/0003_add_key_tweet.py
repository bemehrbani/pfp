# Manually created migration for KeyTweet model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_add_twitter_comment'),
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyTweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_url', models.URLField(help_text='URL of the tweet to comment on')),
                ('author_name', models.CharField(help_text='Display name of the tweet author (e.g. "United Nations")', max_length=200)),
                ('author_handle', models.CharField(help_text='Twitter handle of the author (e.g. "@UN")', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Brief description of the tweet content or why it matters')),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower numbers shown first)')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this key tweet is currently active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(
                    help_text='Task this key tweet belongs to',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='key_tweets',
                    to='tasks.task',
                )),
            ],
            options={
                'verbose_name': 'Key Tweet',
                'verbose_name_plural': 'Key Tweets',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
