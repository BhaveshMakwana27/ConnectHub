# Generated by Django 4.2.3 on 2023-08-05 06:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
        ('Posts', '0004_postlike'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('timeStamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Posts.postcomment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.userprofile')),
            ],
        ),
    ]
