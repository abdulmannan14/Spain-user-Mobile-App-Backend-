# Generated by Django 4.2.13 on 2024-05-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_userdetails_expedition_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='message_sent',
            field=models.BooleanField(default=False),
        ),
    ]
