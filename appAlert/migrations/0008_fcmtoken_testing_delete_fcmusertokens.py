# Generated by Django 4.1.9 on 2023-08-16 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import typing


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appAlert', '0007_alter_fcmusertokens_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMToken_Testing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tokens', models.JSONField(default=list)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fcm_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, typing.Generic),
        ),
        migrations.DeleteModel(
            name='FCMUserTokens',
        ),
    ]
