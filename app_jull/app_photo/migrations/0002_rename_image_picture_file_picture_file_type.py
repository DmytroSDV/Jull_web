# Generated by Django 5.0.4 on 2024-04-27 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_photo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='image',
            new_name='file',
        ),
        migrations.AddField(
            model_name='picture',
            name='file_type',
            field=models.CharField(choices=[('photo', 'Photo'), ('text', 'Text'), ('other', 'Other')], default='other', max_length=10),
        ),
    ]
