# Generated manually for language field addition

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramsession',
            name='language',
            field=models.CharField(
                choices=[('en', 'English'), ('fa', 'فارسی'), ('ar', 'العربية')],
                default='en',
                help_text='Preferred UI language',
                max_length=2,
            ),
        ),
    ]
