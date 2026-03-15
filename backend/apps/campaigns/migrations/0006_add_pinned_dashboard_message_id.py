"""
Django migration: Add pinned_dashboard_message_id to Campaign model.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_add_video_file_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='pinned_dashboard_message_id',
            field=models.BigIntegerField(
                blank=True,
                null=True,
                help_text='Telegram message ID of the pinned campaign dashboard in the channel',
            ),
        ),
    ]
