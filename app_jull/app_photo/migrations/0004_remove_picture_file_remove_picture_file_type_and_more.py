# Generated by Django 5.0.4 on 2024-04-27 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_photo', '0003_alter_picture_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='file',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='file_type',
        ),
        migrations.AddField(
            model_name='picture',
            name='image',
            field=models.ImageField(default='', upload_to='photo_for_users'),
            preserve_default=False,
        ),
    ]
