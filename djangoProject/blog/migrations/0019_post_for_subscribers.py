# Generated by Django 5.0.3 on 2024-04-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='for_subscribers',
            field=models.BooleanField(default=False, verbose_name='Только для подписчиков'),
        ),
    ]