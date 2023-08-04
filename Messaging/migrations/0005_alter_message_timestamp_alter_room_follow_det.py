# Generated by Django 4.2.3 on 2023-08-01 06:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Followers', '0001_initial'),
        ('Messaging', '0004_alter_room_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='room',
            name='follow_det',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_details', to='Followers.follow'),
        ),
    ]
