# Generated by Django 4.1.9 on 2023-08-16 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appAlert', '0006_rename_concreteusertokens_fcmusertokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcmusertokens',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fcm_tokens', to='appAlert.fcmusertokens'),
        ),
    ]
