# Generated by Django 5.0.3 on 2024-05-17 16:41

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_delete_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='Текст'),
        ),
    ]
