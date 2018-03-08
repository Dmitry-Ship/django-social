# Generated by Django 2.0.1 on 2018-02-28 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_follow_is_deleted'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='follow',
            managers=[
                ('follows', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='following',
        ),
        migrations.AlterField(
            model_name='follow',
            name='from_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='to_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to=settings.AUTH_USER_MODEL),
        ),
    ]
