# Generated by Django 4.1.3 on 2022-12-04 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_comment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(default='static/thumbnail/default/default.jpg', upload_to='static/thumbnail/'),
        ),
    ]