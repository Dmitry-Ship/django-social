# Generated by Django 2.0.1 on 2018-03-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20180220_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=140, null=True),
        ),
    ]
