# Generated by Django 5.1.1 on 2024-10-21 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='completion',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taught_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='is_prerequisite_for', to='course.course'),
        ),
        migrations.AddField(
            model_name='enrolled_course',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_users', to='course.course'),
        ),
        migrations.AddField(
            model_name='enrolled_course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='course.course'),
        ),
        migrations.AddField(
            model_name='module',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='completion',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.readingmaterial'),
        ),
        migrations.AddField(
            model_name='session',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='course.course'),
        ),
        migrations.AddField(
            model_name='readingmaterial',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='course.session'),
        ),
        migrations.AddField(
            model_name='completion',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.session'),
        ),
        migrations.AddField(
            model_name='sessioncompletion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='sessioncompletion',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.session'),
        ),
        migrations.AddField(
            model_name='sessioncompletion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sub_course',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_courses', to='course.course'),
        ),
        migrations.AddField(
            model_name='module',
            name='sub_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='course.sub_course'),
        ),
        migrations.AddField(
            model_name='sub_module',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_modules', to='course.module'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='usercourseprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='enrolled_course',
            unique_together={('user', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('student', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='completion',
            unique_together={('session', 'material', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='sessioncompletion',
            unique_together={('course', 'user', 'session')},
        ),
        migrations.AlterUniqueTogether(
            name='sub_course',
            unique_together={('course', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='module',
            unique_together={('order', 'sub_course')},
        ),
        migrations.AlterUniqueTogether(
            name='sub_module',
            unique_together={('order', 'module')},
        ),
        migrations.AlterUniqueTogether(
            name='usercourseprogress',
            unique_together={('user', 'course')},
        ),
    ]
