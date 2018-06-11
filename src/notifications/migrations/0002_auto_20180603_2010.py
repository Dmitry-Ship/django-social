# Generated by Django 2.0.1 on 2018-06-03 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[(1, 'Liked post'), (2, 'Commented post'), (3, 'Liked comment')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notificationcommentliked',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='notifications.Notification'),
        ),
        migrations.AlterField(
            model_name='notificationfollowed',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='notifications.Notification'),
        ),
        migrations.AlterField(
            model_name='notificationpostcommented',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='notifications.Notification'),
        ),
        migrations.AlterField(
            model_name='notificationpostliked',
            name='notification',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='notifications.Notification'),
        ),
    ]
