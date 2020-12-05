# Generated by Django 2.2 on 2020-12-05 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201204_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='user_type',
            field=models.CharField(blank=True, choices=[('m', 'Moderator'), ('a', 'Author'), ('r', 'Reader')], max_length=1, null=True),
        ),
    ]
