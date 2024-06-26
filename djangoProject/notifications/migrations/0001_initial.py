# Generated by Django 5.0.3 on 2024-05-14 19:11

import django.db.models.deletion
import django.utils.timezone
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
                ('sender_name', models.CharField(default='', max_length=255, verbose_name='Имя отправителя')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('text', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время')),
                ('is_new', models.BooleanField(default=True, verbose_name='Новое уведомление')),
                ('viewed', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('sender', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
