# Generated by Django 2.2 on 2021-01-20 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210116_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='banned',
            field=models.BooleanField(default=False),
        ),
    ]
