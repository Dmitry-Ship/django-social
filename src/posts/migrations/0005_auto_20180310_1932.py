# Generated by Django 2.0.1 on 2018-03-10 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20180305_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(default='hello', max_length=140),
            preserve_default=False,
        ),
    ]