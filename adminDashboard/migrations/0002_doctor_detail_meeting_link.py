# Generated by Django 4.1.2 on 2022-11-03 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor_detail',
            name='meeting_link',
            field=models.URLField(blank=True),
        ),
    ]
