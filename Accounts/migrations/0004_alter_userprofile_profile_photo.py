# Generated by Django 4.2.3 on 2023-08-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_alter_userprofile_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.ImageField(default='user/default/image.png', upload_to='user/images/'),
        ),
    ]
