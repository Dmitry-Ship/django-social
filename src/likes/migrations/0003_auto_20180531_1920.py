# Generated by Django 2.0.1 on 2018-05-31 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_auto_20180530_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentlike',
            old_name='comment',
            new_name='target',
        ),
        migrations.RenameField(
            model_name='postlike',
            old_name='post',
            new_name='target',
        ),
    ]