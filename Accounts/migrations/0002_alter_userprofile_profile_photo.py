# Generated by Django 4.2.3 on 2023-08-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.ImageField(default='static/default/image.png', upload_to='user/images/'),
        ),
    ]