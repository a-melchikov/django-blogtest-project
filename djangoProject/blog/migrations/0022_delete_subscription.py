# Generated by Django 5.0.3 on 2024-05-13 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_favorite_options_alter_favorite_post_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
