# Generated by Django 4.2.9 on 2024-01-22 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoringApp", "0007_remove_websiteshistory_error_end_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="website",
            name="status_code",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]