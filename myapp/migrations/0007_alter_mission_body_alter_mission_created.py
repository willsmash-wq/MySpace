# Generated by Django 4.2.1 on 2023-05-24 02:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_mission_body_alter_mission_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='mission',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 24, 2, 26, 30, 330515, tzinfo=datetime.timezone.utc)),
        ),
    ]
