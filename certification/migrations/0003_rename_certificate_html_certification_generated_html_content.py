# Generated by Django 5.1.1 on 2024-10-26 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0002_certification_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='certificate_html',
            new_name='generated_html_content',
        ),
    ]
