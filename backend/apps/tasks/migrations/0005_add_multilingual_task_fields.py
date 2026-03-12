# Manually created migration for multilingual content fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_add_petition_mass_email_task_types'),
    ]

    operations = [
        # Task: title_fa, title_ar
        migrations.AddField(
            model_name='task',
            name='title_fa',
            field=models.CharField(blank=True, default='', help_text='Task title (Farsi)', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='title_ar',
            field=models.CharField(blank=True, default='', help_text='Task title (Arabic)', max_length=200),
        ),
        # Task: description_fa, description_ar
        migrations.AddField(
            model_name='task',
            name='description_fa',
            field=models.TextField(blank=True, default='', help_text='Detailed task description (Farsi)'),
        ),
        migrations.AddField(
            model_name='task',
            name='description_ar',
            field=models.TextField(blank=True, default='', help_text='Detailed task description (Arabic)'),
        ),
        # Task: instructions_fa, instructions_ar
        migrations.AddField(
            model_name='task',
            name='instructions_fa',
            field=models.TextField(blank=True, default='', help_text='Instructions (Farsi)'),
        ),
        migrations.AddField(
            model_name='task',
            name='instructions_ar',
            field=models.TextField(blank=True, default='', help_text='Instructions (Arabic)'),
        ),
    ]
