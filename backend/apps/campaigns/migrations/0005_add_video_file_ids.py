"""Add video_file_id fields to Campaign model for Telegram file caching."""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0004_add_channel_broadcasting_branding'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='video_file_id_en',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Telegram file_id for English 100 Faces video',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='campaign',
            name='video_file_id_fa',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Telegram file_id for Farsi 100 Faces video',
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name='campaign',
            name='video_file_id_ar',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Telegram file_id for Arabic 100 Faces video',
                max_length=255,
            ),
        ),
    ]
