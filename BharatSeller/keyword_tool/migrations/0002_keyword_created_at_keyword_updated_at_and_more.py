# Generated by Django 5.1.3 on 2024-11-12 07:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyword_tool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='keyword',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='difficulty',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
