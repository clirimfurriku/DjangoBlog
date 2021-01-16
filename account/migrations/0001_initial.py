# Generated by Django 2.2 on 2021-01-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=120, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user_type', models.CharField(blank=True, choices=[('a', 'Author'), ('r', 'Reader')], max_length=1, null=True)),
                ('bio', models.CharField(blank=True, max_length=2048, null=True)),
                ('twitter', models.CharField(blank=True, max_length=128, null=True)),
                ('instagram', models.CharField(blank=True, max_length=128, null=True)),
                ('facebook', models.CharField(blank=True, max_length=128, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]