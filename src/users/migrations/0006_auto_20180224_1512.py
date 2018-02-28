# Generated by Django 2.0.1 on 2018-02-24 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_userprofile_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='relationships', through='users.Follow', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='from_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to='users.UserProfile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='to_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to='users.UserProfile'),
        ),
    ]
