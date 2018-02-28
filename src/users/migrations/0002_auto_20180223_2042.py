# Generated by Django 2.0.1 on 2018-02-23 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to=settings.AUTH_USER_MODEL, unique=True)),
                ('to_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, through='users.Follow', to='users.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('from_person', 'to_person')},
        ),
    ]
