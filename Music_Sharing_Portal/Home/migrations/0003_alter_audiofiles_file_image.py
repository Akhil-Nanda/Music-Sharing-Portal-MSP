# Generated by Django 4.2.2 on 2023-06-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_alter_audiofiles_file_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofiles',
            name='file_image',
            field=models.ImageField(upload_to='image/'),
        ),
    ]
