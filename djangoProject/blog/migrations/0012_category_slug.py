# Generated by Django 5.0.3 on 2024-04-17 16:24

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_category_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='name', unique=True, verbose_name='Slug'),
        ),
    ]
