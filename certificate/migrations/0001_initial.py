# Generated by Django 5.0.9 on 2024-10-16 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('certificate_url', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]