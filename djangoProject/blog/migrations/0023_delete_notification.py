# Generated by Django 5.0.3 on 2024-05-14 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_delete_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
