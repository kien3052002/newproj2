# Generated by Django 4.1.3 on 2022-12-05 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_seen_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='seen_by',
        ),
    ]
