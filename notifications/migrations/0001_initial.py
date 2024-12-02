# Generated by Django 5.0.9 on 2024-11-18 10:55

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_new', models.BooleanField(default=True)),
                ('is_modified', models.BooleanField(default=False)),
                ('is_important', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('read_by', models.ManyToManyField(blank=True, related_name='read_notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]