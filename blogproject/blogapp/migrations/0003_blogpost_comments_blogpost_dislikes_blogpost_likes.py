# Generated by Django 5.2.4 on 2025-07-24 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='comments',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='dislikes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
