# Generated by Django 4.2.3 on 2023-07-31 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Messaging', '0003_room_follow_det_alter_room_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.SlugField(default='chat'),
        ),
    ]