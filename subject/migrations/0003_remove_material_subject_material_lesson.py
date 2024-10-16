# Generated by Django 5.0.9 on 2024-10-11 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0002_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='subject',
        ),
        migrations.AddField(
            model_name='material',
            name='lesson',
            field=models.ForeignKey(default=0.0005002501250625312, on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='subject.lesson'),
            preserve_default=False,
        ),
    ]