# Manually created migration for multilingual campaign fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        # Campaign: name_fa, name_ar
        migrations.AddField(
            model_name='campaign',
            name='name_fa',
            field=models.CharField(blank=True, default='', help_text='Campaign name (Farsi)', max_length=200),
        ),
        migrations.AddField(
            model_name='campaign',
            name='name_ar',
            field=models.CharField(blank=True, default='', help_text='Campaign name (Arabic)', max_length=200),
        ),
        # Campaign: short_description_fa, short_description_ar
        migrations.AddField(
            model_name='campaign',
            name='short_description_fa',
            field=models.CharField(blank=True, default='', help_text='Short description (Farsi)', max_length=500),
        ),
        migrations.AddField(
            model_name='campaign',
            name='short_description_ar',
            field=models.CharField(blank=True, default='', help_text='Short description (Arabic)', max_length=500),
        ),
    ]
